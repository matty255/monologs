def profile_info(request):
    if request.user.is_authenticated:
        profile_picture = request.user.profile_picture
        profile_status = request.user.profile_status
    else:
        profile_picture = None
        profile_status = None

    return {"profile_picture": profile_picture, "profile_status": profile_status}
