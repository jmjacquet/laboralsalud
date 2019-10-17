# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from itertools import chain
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape


      
class UsuarioCambiarPasswdForm(forms.Form):      
      new_password = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=20,label='Contraseña Nueva') 
      reenter_password = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=20,label='Reingresar Contraseña') 
     
      def clean(self):
         new_password = self.cleaned_data.get('new_password')
         reenter_password = self.cleaned_data.get('reenter_password')
                   
         if new_password and new_password!=reenter_password:
            self._errors['reenter_password'] = [u'Debe ingresar la misma contraseña.']         
         #get the user object and check from old_password list if any one matches with the new password raise error(read whole answer you would know) 
         return self.cleaned_data #don't forget this.