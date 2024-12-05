# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
import os
# =================================
from palindrome_src.public.forms import PalindromeForm
# =================================
from palindrome_src.extensions import login_manager
from palindrome_src.user.models import User
# =================================
from environs import Env

env = Env()
env.read_env()

path = env.str("PROJECT_PATH")

blueprint = Blueprint("public", __name__, static_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))

# ================================================================
# ============================  Home  ============================
# ================================================================

@blueprint.route('/')
def home():
    return render_template('public/home.html')

# Recursive function to create structured data with indentation levels
def get_directory_structure(rootdir, level=0):
    structure = []
    for item in sorted(os.listdir(rootdir)):
        item_path = os.path.join(rootdir, item)
        if os.path.isdir(item_path):
            structure.append({
                "name": item,
                "type": "folder",
                "level": level,
                "children": get_directory_structure(item_path, level + 1)
            })
        else:
            structure.append({
                "name": item,
                "type": "file",
                "path": item_path,
                "level": level
            })
    return structure

@blueprint.route('/tree', methods=['GET'])
def tree_view():
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/thegreatest/PyFolder2/Flask_Khpi/palindrome_src'))
    directory_structure = get_directory_structure(root_directory)
    return render_template("public/tree.html", dir_structure=directory_structure)

@blueprint.route('/api/file_content', methods=['GET'])
def get_file_content():
    filepath = request.args.get('path')
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)})

# ================================================================
# ========================== Palindrome  =========================
# ================================================================

def is_palindrome(number: str) -> bool:
    return number == number[::-1]

@blueprint.route("/palindrom", methods=["GET", "POST"])
def data_entry():
    form = PalindromeForm()
    if form.validate_on_submit():
        number = form.number.data
        if is_palindrome(number):
            flash("Yes! It's a palindrome!", "success")
            image = os.path.join("img", "yes.png")
        else:
            flash("No! It's not a palindrome.", "danger")
            image = os.path.join("img", "no.png")
        return render_template("public/data_output.html", number=number, image=image)
    return render_template("public/data_entry.html", form=form)


