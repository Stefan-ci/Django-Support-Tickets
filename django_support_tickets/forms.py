from django import forms



class TicketForm(forms.Form):
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        )
    )
    
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        )
    )





class TicketCommentForm(forms.Form):
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-sm",
            }
        )
    )
    
    comment = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-sm",
            }
        )
    )
