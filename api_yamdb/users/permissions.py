from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        del view
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )

    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Any,
    ) -> bool:
        del view, obj
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class AuthUserAdminModeratorPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Any,
    ) -> bool:
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator'
                )
            )
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        del view
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Any,
    ) -> bool:
        del view, obj
        return request.method in permissions.SAFE_METHODS
