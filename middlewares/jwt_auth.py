from datetime import datetime, timedelta, timezone
from flask import abort, request, redirect, url_for
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, create_access_token, get_jwt_identity, set_access_cookies
from constants import USER_ROUTES, ORGANIZATION_ROUTES, ADMIN_ROUTES, RESEARCH_ROUTES, COMPONENTS_ROUTES, PROTECTED_API_ROUTES, PROTECTED_ROUTES

jwt = JWTManager()

def check_jwt_authentication():
    if request.endpoint in PROTECTED_ROUTES:
        try:
            verify_jwt_in_request()
            payload = get_jwt()

            role = payload.get("role")
            if not role:
                abort(403)
                
            if request.endpoint not in PROTECTED_API_ROUTES:
                if request.endpoint in COMPONENTS_ROUTES:
                    return

                if request.endpoint in RESEARCH_ROUTES:
                    return
                
                if role == "admin":
                    if request.endpoint not in ADMIN_ROUTES:
                        return redirect(url_for("admin.dashboard"))
                    return
                
                if request.endpoint in ADMIN_ROUTES:
                    if role == "ervaringsdeskundige":
                        return redirect(url_for("user.dashboard"))
                    else:
                        return redirect(url_for("organization.dashboard")) 
                    
                if role == "ervaringsdeskundige" and request.endpoint not in USER_ROUTES :
                    return redirect(url_for("user.dashboard"))
                    
                if role == "organisatie" and request.endpoint not in ORGANIZATION_ROUTES:
                    return redirect(url_for("organization.dashboard")) 
        except Exception as e:
            print(e)
            abort(401)

def refresh_jwt(response):
    """
    Get token expiration time -> Calculate current time -> If token expires within 15 minutes, give a new token in response -> Else just return the response from the function that preceded this after_request
    """
    try:
        if request.endpoint == "authorization.logout": # Geen refresh na logout
            return response
        
        payload = get_jwt()
        exp_timestamp = payload.get("exp")
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=15))
        
        if target_timestamp > exp_timestamp:    
            access_token = create_access_token(
                identity=get_jwt_identity(),
                additional_claims={"role": payload.get("role")}
            )
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response