# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from itertools import chain
from django.utils.safestring import mark_safe
      
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


class CHKMultiplePermisos(forms.CheckboxSelectMultiple):   
     def __init__(self,usuario=None, *args, **kwargs):        
        self.usuario = usuario
        super(CHKMultiplePermisos, self).__init__(*args, **kwargs)

     def render(self, name, value, attrs=None, choices=()):
         if value is None: value = []
         
         has_id = attrs and 'id' in attrs        
         usuario = self.usuario
         if usuario:
          permisos_ids = usuario.permisos.values_list('pk', flat=True)
         else:
          permisos_ids = []         
         final_attrs = self.build_attrs(attrs, {'name': name})
         output = [u'' ]
         # Normalize to strings
         str_values = set([force_unicode(v) for v in value])
         
         apps=UsuCategPermisos.objects.all().order_by('orden')    
                                 
         for i,categoria in enumerate(apps):  
             output.append(u'<div class="col-sm-4 cerca"> ' )
             output.append(u'<div class="panel panel-primary">')
             output.append(u'<div class="panel-heading"><strong>%s </strong></div>' % (categoria))
             output.append(u'<div class="panel-body">')
             del self.choices
             self.choices = []                          

             permisos = UsuPermiso.objects.filter(categoria=categoria)             

             for permiso in permisos:
                 self.choices.append((permiso.id_permiso,permiso.permiso))
             # output.append(u'<div class="col-sm-4"> ' )
             for j, (option_value, option_label) in enumerate(chain(self.choices, choices)):
                 if has_id:
                     final_attrs = dict(final_attrs, id='%s_%s_%s' % (attrs['id'], j,i))
                     label_for = u' for="%s"' % final_attrs['id']
                 else:
                     label_for = ''
                 cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                 option_value = force_unicode(option_value)
                 rendered_cb = cb.render(name, option_value)
                 option_label = conditional_escape(force_unicode(option_label))

                 output.append(u'<p><label%s>%s %s</label></p>' % (label_for, rendered_cb, option_label))

             output.append(u' </div>')
             output.append(u' </div>')
             output.append(u' </div>')                
         return mark_safe(u'\n'.join(output))

class CHKMultipleEmpresas(forms.CheckboxSelectMultiple):   
     def __init__(self,usuario=None, *args, **kwargs):        
        self.usuario = usuario
        super(CHKMultipleEmpresas, self).__init__(*args, **kwargs)

     def render(self, name, value, attrs=None, choices=()):
         if value is None: value = []
         
         has_id = attrs and 'id' in attrs        
         usuario = self.usuario
         if usuario:
          empresas_ids = usuario.empresas.values_list('pk', flat=True)
         else:
          empresas_ids = []         
         final_attrs = self.build_attrs(attrs, {'name': name})
         output = [u'' ]
         # Normalize to strings
         str_values = set([force_unicode(v) for v in value])
         
         output.append(u'<div class="col-sm-12"> ' )
         output.append(u'<div class="panel panel-primary">')
         output.append(u'<div class="panel-heading"><strong>EMPRESAS</strong></div>')
         output.append(u'<div class="panel-body">')
         
         apps=UsuCategPermisos.objects.all().order_by('orden')    
         del self.choices
         self.choices = []                          

         empresas = ent_empresa.objects.filter(baja=False)             

         for e in empresas:
             self.choices.append((e.pk,e.razon_social))
         # output.append(u'<div class="col-sm-4"> ' )
         for j, (option_value, option_label) in enumerate(chain(self.choices, choices)):
             if has_id:
                 final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], j))
                 label_for = u' for="%s"' % final_attrs['id']
             else:
                 label_for = ''
             cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
             option_value = force_unicode(option_value)
             rendered_cb = cb.render(name, option_value)
             option_label = conditional_escape(force_unicode(option_label))

             output.append(u'<p><label%s>%s %s</label></p>' % (label_for, rendered_cb, option_label))

         output.append(u' </div>')
         output.append(u' </div>')
         output.append(u' </div>')
                                 
         # for i,categoria in enumerate(apps):  
         #     output.append(u'<div class="col-sm-3"> ' )
         #     output.append(u'<div class="panel panel-body panel-primary panel_centrado">')
         #     output.append(u'<div class="panel-heading"><strong>%s </strong></div>' % (categoria))
         #     output.append(u'<div class="panel-body">')
         #     del self.choices
         #     self.choices = []                          

         #     permisos = ent_empresa.objects.filter(categoria=categoria)             

         #     for permiso in permisos:
         #         self.choices.append((permiso.id_permiso,permiso.permiso))
         #     # output.append(u'<div class="col-sm-4"> ' )
         #     for j, (option_value, option_label) in enumerate(chain(self.choices, choices)):
         #         if has_id:
         #             final_attrs = dict(final_attrs, id='%s_%s_%s' % (attrs['id'], j,i))
         #             label_for = u' for="%s"' % final_attrs['id']
         #         else:
         #             label_for = ''
         #         cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
         #         option_value = force_unicode(option_value)
         #         rendered_cb = cb.render(name, option_value)
         #         option_label = conditional_escape(force_unicode(option_label))

         #         output.append(u'<p><label%s>%s %s</label></p>' % (label_for, rendered_cb, option_label))

         #     output.append(u' </div>')
         #     output.append(u' </div>')
         #     output.append(u' </div>')                
         return mark_safe(u'\n'.join(output))         


class UsuarioForm(forms.ModelForm):       
    nombre = forms.CharField(label=u'Nombre',required = True)
    usuario = forms.CharField(label=u'Usuario',required = True)        
    email = forms.EmailField(max_length=50,label='E-Mail',required = False)     
    permisos = forms.ModelMultipleChoiceField(queryset=UsuPermiso.objects.all(), required=False, widget=CHKMultiplePermisos())    
    empresas =forms.ModelMultipleChoiceField(queryset=ent_empresa.objects.filter(baja=False), required=False, widget=CHKMultipleEmpresas())    
    class Meta:
    	model = UsuUsuario	
        exclude = ['baja','password','numero_documento','empresa']

    def __init__(self,request,usuario, *args, **kwargs):                
        super(UsuarioForm, self).__init__(*args, **kwargs)            
        self.fields['permisos'].widget=CHKMultiplePermisos(usuario)        
        self.fields['empresas'].widget=CHKMultipleEmpresas(usuario)    
