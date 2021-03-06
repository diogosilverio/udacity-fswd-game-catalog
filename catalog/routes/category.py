""" Provides routes for Category listing and detail """
from flask import render_template, request, flash, redirect, jsonify

from catalog.infra.flask_factory import app
from catalog.models.category import Category
from catalog.services.category_service import CategoryService
from catalog.services.game_service import GameService

from .security import protected, check_owner


@app.route('/category', methods=['GET'])
def category():
    categories = CategoryService().all()
    return render_template("category_index.html", categories=categories)


@app.route('/category.json', methods=['GET'])
def category_json():
    return jsonify([c.to_short_json() for c in CategoryService().all()])


@app.route('/category/new', methods=['GET'])
@protected
def category_form():
    return render_template("category_form.html", target_url="/category/new",
                           category=Category(name='', description=''))


@app.route('/category/new', methods=['POST'])
@protected
def category_new():
    new_category = validate_category()

    if new_category:
        if CategoryService().new(new_category):
            flash('New category added', 'success')
        else:
            flash('Error adding category', 'danger')

    return redirect('/category')


@app.route('/category/<int:cid>', methods=['GET'])
def category_detail(cid):
    cat = CategoryService().find_by_id(cid)
    if not cat:
        flash('Category not found', 'warning')
        return redirect('/category')

    games = GameService().find_by_category(cat)

    return render_template("category.html", category=cat, games=games)


@app.route('/category/<int:cid>.json', methods=['GET'])
def category_detail_json(cid):
    cat = CategoryService().find_by_id(cid, True)

    if not cat:
        return jsonify({}), 404

    return jsonify(cat.to_json())


@app.route('/category/<int:cid>/delete', methods=['POST'])
@protected
@check_owner(Category)
def delete_category(cid):
    category_service = CategoryService()
    cat = category_service.find_by_id(cid)

    if not cat:
        flash('Category does not exists', 'warning')

    try:
        category_service.delete(cat)
        flash('Category removed', 'info')
    except Exception as exc:
        flash("Error deleting category: %s" % exc.message, 'danger')

    return redirect('/category')


@app.route('/category/<int:cid>/update', methods=['GET'])
@protected
@check_owner(Category)
def update_category_form(cid):
    cat = CategoryService().find_by_id(cid)

    if not cat:
        flash('Category does not exists')
        return redirect('/category')

    return render_template("category_form.html", category=cat,
                           target_url="/category/%d/update" % cat.id)


@app.route('/category/<int:cid>/update', methods=['POST'])
@protected
@check_owner(Category)
def update_category(cid):
    updated_category = validate_category()

    if updated_category:
        updated_category.id = cid

        if CategoryService().new(updated_category):
            flash('Category updated', 'success')
        else:
            flash('Error updating category', 'danger')

    return redirect('/category')


def validate_category():
    name = request.form['name']
    description = request.form['description']
    invalid = False

    if not name or len(name.strip()) < 3:
        invalid = True
        flash('Type a valid name with three or more characters', 'warning')

    if not description or len(description.strip()) == 0:
        invalid = True
        flash('Type some description', 'warning')

    if not invalid:
        return Category(name=name, description=description)
    else:
        return None
