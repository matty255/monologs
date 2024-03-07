def profile_info(request):
    if request.user.is_authenticated:
        user = request.user
        profile_picture = user.profile_picture.url if user.profile_picture else None
        profile_status = user.profile_status
    else:
        profile_picture = None
        profile_status = None

    return {"profile_picture": profile_picture, "profile_status": profile_status}
