from flask import Blueprint
from .tasks import add, flask_app_context,remind

bp = Blueprint("test", __name__, url_prefix='/test')


@bp.route('/testAdd', methods=["GET"])
def test_add():
    """
    测试相加
    :return:
    """
    result = add.apply_async(args=(5,))
    # result = add.delay(1, 2)
    # return result.get(timeout=1)
    return result.get()


@bp.route('/testFlaskAppContext', methods=["GET"])
def test_flask_app_context():
    """
    测试相加
    :return:
    """
    result = flask_app_context.delay()
    return result.get(timeout=1).replace('<Config', '')

@bp.route('/email',methods=["GET"])
def mail_to():
    re = remind('1111')
    return re
