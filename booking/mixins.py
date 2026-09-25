from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    """
    Mixin to check if the logged-in user is the owner of the object.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.customer != request.user:
            raise PermissionDenied("You do not have permission to access this object.")
        return super().dispatch(request, *args, **kwargs)
    
class LoginRequiredMixin:
    """
    Mixin to ensure that the user is logged in.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this page.")
        return super().dispatch(request, *args, **kwargs)
    
class UserIsStaffMixin:
    """
    Mixin to check if the logged-in user is a staff member.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You must be a staff member to access this page.")
        return super().dispatch(request, *args, **kwargs)

class IsCustomerOwnerMixin:
    """
    Mixin to check if the logged-in user is the owner of the customer object.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise PermissionDenied("You do not have permission to access this object.")
        return super().dispatch(request, *args, **kwargs)

class UserIsCustomerMixin:
    """
    Mixin to check if the logged-in user is a customer.
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer'):
            raise PermissionDenied("You must be a customer to access this page.")
        return super().dispatch(request, *args, **kwargs)