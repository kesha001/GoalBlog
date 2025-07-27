from app.api.auth import user_auth, token_auth
from app.api import api_bp
from app import db


@api_bp.route("/get_token", methods=['GET'])
@user_auth.login_required
def get_token():
    token = user_auth.current_user().get_token()
    db.session.commit()

    return {"token": token}


@api_bp.route("/revoke_token", methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    user_auth.current_user().revoke_token()
    db.session.commit()

    return "", 204