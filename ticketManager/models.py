from django.db import models

from django.conf import settings

from django.utils.translation import gettext_lazy as _



class Ticket(models.Model):
    # TODO :
    # Check that the assigned_to user is a technitian
    # Check that a created_by user is a regular employee

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
        ordering = '-created_at'
        permissions = [
            ('can_change_status_only',_('Can only edit status of the ticket. reserved For Technitians')),
            ('can_change_title_desc_only', _('Can only edit the title and description. For regular employe'))
            ('can_assign_technician', _('Can chose who is in charge of the ticket. For the admin only'))

        ] 

    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        ON_HOLD = 'ON_HOLD', _('On Hold')
        FINISHED = 'FINISHED', _('Finished')
        CLOSED = 'CLOSED', _('Closed')


    title = models.CharField(_('title'), max_length=255, blank=False)
    description = models.TextField(_('description'), max_length=600, blank=False)
    status = models.CharField(choices= Status.choices, default=Status.OPEN )
    
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, related_name='assigned_tickets')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now=True)

    def _allowed_transitions(self):
        transitions ={
            self.Status.OPEN : [self.Status.IN_PROGRESS, self.Status.FINISHED],
            self.Status.IN_PROGRESS : [self.Status.ON_HOLD, self.Status.FINISHED],
            self.Status.ON_HOLD : [self.Status.OPEN, self.Status.IN_PROGRESS, self.Status.FINISHED],
            self.Status.FINISHED : [self.Status.CLOSED],
            self.Status.CLOSED : []
        }

        return transitions.get(self.status)
    
    def transition(self, new_transition):
        """
        Take care of the tickets status of transitions
        Args:
            - new_transition : Type of Status, is the new status of the ticket
        Returns:
            - True if the transition is done
            - Raises a ValueError if not
        """
        if new_transition in self._allowed_transitions(self.status):
            self.status = new_transition
            self.save()
            return True
        raise ValueError(_('Transition not allowed'))

    
