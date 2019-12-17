# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext,Context
from django.shortcuts import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId,usuario_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.db.models import Q,Sum,Count,FloatField,Func
from django.forms.models import inlineformset_factory,BaseInlineFormSet,formset_factory
from django.utils.functional import curry 

from .models import *
from general.views import VariablesMixin
from usuarios.views import tiene_permiso
from .forms import AusentismoForm,PatologiaForm,DiagnosticoForm,ConsultaAusentismos,ControlesDetalleForm
############ AUSENTISMOS ############################

class AusentismoView(VariablesMixin,ListView):
    model = ausentismo
    template_name = 'ausentismos/ausentismo_listado.html'
    context_object_name = 'ausentismos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'aus_pantalla'):
            return redirect(reverse('principal'))
        return super(AusentismoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoView, self).get_context_data(**kwargs)
        busq = None        
        if self.request.POST:
            busq = self.request.POST
        else:
            if 'ausentismos' in self.request.session:
                busq = self.request.session["ausentismos"]
        form = ConsultaAusentismos(busq or None,request=self.request)   
        fdesde=hoy()
        fhasta=finMes()
        ausentismos = ausentismo.objects.filter(baja=False,empleado__empresa__pk__in=empresas_habilitadas(self.request))
        ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))
        ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))                                
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            estado = form.cleaned_data['estado']
          
            ausentismos = ausentismo.objects.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

            if int(estado) == 1:  
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__gte=hoy(),tipo_ausentismo=1)|Q(art_fcronhasta__gte=hoy(),tipo_ausentismo__gte=2))
            elif int(estado) == 2:  
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__lt=hoy(),tipo_ausentismo=1)|Q(art_fcronhasta__lt=hoy(),tipo_ausentismo__gte=2))
            elif int(estado) == 0: 
                if fdesde:                
                    ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))                         
                if fhasta:                
                    ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))                                
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))
            
            if int(tipo_ausentismo) > 0: 
                if int(tipo_ausentismo)==11:
                    ausentismos = ausentismos.filter(Q(aus_diascaidos__lte=30)|Q(art_diascaidos__lte=30))
                elif int(tipo_ausentismo)==12:
                    ausentismos = ausentismos.filter(Q(aus_diascaidos__gt=30)|Q(art_diascaidos__gt=30))                    
                else:
                    ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))            
            self.request.session["ausentismos"] = self.request.POST
        else:
            self.request.session["ausentismos"] = None        
        context['form'] = form
        context['ausentismos'] = ausentismos.select_related('empleado','empleado__empresa','aus_grupop','aus_diagn')
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class ControlesDetalleFormSet(BaseInlineFormSet): 
    pass  
ControlDetalleFormSet = inlineformset_factory(ausentismo, ausentismo_controles,form=ControlesDetalleForm,formset=ControlesDetalleFormSet, can_delete=True,extra=0,min_num=1)

class AusentismoCreateView(VariablesMixin,CreateView):
    form_class = AusentismoForm
    template_name = 'ausentismos/ausentismo_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'aus_abm'):
            return redirect(reverse('principal'))
        return super(AusentismoCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)                               
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)                       
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)        

    def form_valid(self, form):                                
        self.object = form.save(commit=False)                           
        self.object.usuario = usuario_actual(self.request)             
        self.object.save()      
        return super(AusentismoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AusentismoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(AusentismoCreateView, self).get_initial()               
        initial['request'] = self.request        
        initial['tipo_form'] = 'ALTA'
        return initial    

    def form_invalid(self, form):                                                       
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return reverse('ausentismo_listado')

    
class AusentismoEditView(VariablesMixin,UpdateView):
    form_class = AusentismoForm
    model = ausentismo
    pk_url_kwarg = 'id'
    template_name = 'ausentismos/ausentismo_form.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'aus_abm'):
            return redirect(reverse('principal'))
        return super(AusentismoEditView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)                               
        form.fields['empleado'].widget.attrs['disabled'] = True                    
        controles_detalle = ControlDetalleFormSet(instance=self.object,prefix='formDetalle')                                
        return self.render_to_response(self.get_context_data(form=form,controles_detalle = controles_detalle))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        controles_detalle = ControlDetalleFormSet(self.request.POST,instance=self.object,prefix='formDetalle')       
        if form.is_valid() and controles_detalle.is_valid():
            return self.form_valid(form, controles_detalle)
        else:
            print '%s error '%(form.errors)
            return self.form_invalid(form,controles_detalle)  

    def form_valid(self, form,controles_detalle):                                
        self.object.save()
        controles_detalle.instance = self.object
        controles_detalle.ausentismo = self.object.id        
        controles_detalle.save()   
        return HttpResponseRedirect(reverse('ausentismo_listado'))

    def form_invalid(self, form,controles_detalle):
        # print form.errors
        return self.render_to_response(self.get_context_data(form=form,controles_detalle = controles_detalle))        

    def get_form_kwargs(self):
        kwargs = super(AusentismoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(AusentismoEditView, self).get_initial()                      
        initial['request'] = self.request  
        initial['tipo_form'] = 'EDICION'
        return initial  

    def get_success_url(self): 
        messages.success(self.request, u'Los datos se guardaron con éxito!')       
        return reverse('ausentismo_listado')          


class AusentismoVerView(VariablesMixin,DetailView):
    model = ausentismo
    pk_url_kwarg = 'id'
    context_object_name = 'a'
    template_name = 'ausentismos/ausentismo_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(AusentismoVerView, self).dispatch(*args, **kwargs)        


@login_required 
def ausentismo_baja_alta(request,id):
    if not tiene_permiso(request,'aus_abm'):
            return redirect(reverse('principal'))
    aus = ausentismo.objects.get(pk=id)     
    aus.baja = not aus.baja
    aus.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("ausentismo_listado"))     


############ PATOLOGIAS ############################

class PatologiaView(VariablesMixin,ListView):
    model = aus_patologia
    template_name = 'ausentismos/patologia_listado.html'
    context_object_name = 'patologias'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'pat_pantalla'):
            return redirect(reverse('principal'))
        return super(PatologiaView, self).dispatch(*args, **kwargs)
    

class PatologiaCreateView(VariablesMixin,AjaxCreateView):
    form_class = PatologiaForm
    template_name = 'fm/entidades/form_patologia.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'pat_pantalla'):
            return redirect(reverse('principal'))
        return super(PatologiaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(PatologiaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(PatologiaCreateView, self).get_initial()               
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(PatologiaCreateView, self).form_invalid(form)


class PatologiaEditView(VariablesMixin,AjaxUpdateView):
    form_class = PatologiaForm
    model = aus_patologia
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_patologia.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'pat_pantalla'):
            return redirect(reverse('principal'))
        return super(PatologiaEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(PatologiaEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PatologiaEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(PatologiaEditView, self).get_initial()                      
        return initial            


# class PatologiaVerView(VariablesMixin,DetailView):
#     model = ent_art
#     pk_url_kwarg = 'id'
#     context_object_name = 'art'
#     template_name = 'entidades/art_detalle.html'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs): 
#         return super(ARTVerView, self).dispatch(*args, **kwargs)        


# @login_required 
# def art_baja_alta(request,id):
#     art = ent_art.objects.get(pk=id)     
#     art.baja = not art.baja
#     art.save()       
#     messages.success(request, u'¡Los datos se guardaron con éxito!')
#     return HttpResponseRedirect(reverse("art_listado")) 


############ DIAGNOSTICOS ############################

class DiagnosticoView(VariablesMixin,ListView):
    model = aus_diagnostico
    template_name = 'ausentismos/diagnostico_listado.html'
    context_object_name = 'diagnosticos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'diag_pantalla'):
            return redirect(reverse('principal'))
        return super(DiagnosticoView, self).dispatch(*args, **kwargs)
    

class DiagnosticoCreateView(VariablesMixin,AjaxCreateView):
    form_class = DiagnosticoForm
    template_name = 'fm/entidades/form_diagnostico.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'diag_pantalla'):
            return redirect(reverse('principal'))
        return super(DiagnosticoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(DiagnosticoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(DiagnosticoCreateView, self).get_initial()               
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(DiagnosticoCreateView, self).form_invalid(form)


class DiagnosticoEditView(VariablesMixin,AjaxUpdateView):
    form_class = DiagnosticoForm
    model = aus_diagnostico
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_diagnostico.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'diag_pantalla'):
            return redirect(reverse('principal'))
        return super(DiagnosticoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(DiagnosticoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(DiagnosticoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(DiagnosticoEditView, self).get_initial()                      
        return initial            



import csv, io
   
import datetime
def ausencias_importar(request):
    data = {}    
   
    if request.method == 'POST':  
        csv_file = request.FILES["archivo"]
        #tabla = request.POST['username']     
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("ausencias_importar"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("ausencias_importar"))

        file_data = csv_file.read().decode("utf8", "ignore")

        lines = file_data.split("\n")
        cant = len(lines)
        
        for index,line in enumerate(lines):                      
            campos = line.split(";")
            legajo = campos[0].strip()                
            dni = campos[1].strip()                
            empleado = ent_empleado.objects.get(nro_doc=dni)

            if campos[2]=='':
                fecha_creacion = None
            else:
                fecha_creacion = datetime.datetime.strptime(campos[2], "%d/%m/%Y").date()                
            
            tipoa = campos[3].strip()                       
            if tipoa=='':
                tipoa = None
            else:
                ta=dict(TIPO_AUSENCIA)        
                tipoa = [k for k, v in ta.items() if v == tipoa][0]

            if (campos[4].strip() == 'Si'): 
                aus_control = 'S' 
            else: 
                aus_control = 'N'
             
            if campos[5]=='':
                aus_fcontrol = None
            else:
                aus_fcontrol = datetime.datetime.strptime(campos[5], "%d/%m/%Y").date()                
            if (campos[6].strip() == 'Si'): 
                aus_certificado = 'S' 
            else: 
                aus_certificado = 'N'

            if campos[7]=='':
                aus_fcertif = None
            else:
                aus_fcertif = datetime.datetime.strptime(campos[7], "%d/%m/%Y").date()                
            if campos[8]=='':
                aus_fentrega_certif = None
            else:
                aus_fentrega_certif = datetime.datetime.strptime(campos[8], "%d/%m/%Y").date()                
            
            if campos[9]=='':
                aus_fcrondesde = None
            else:
                aus_fcrondesde = datetime.datetime.strptime(campos[9], "%d/%m/%Y").date()                
            if campos[10]=='':
                aus_fcronhasta = None
            else:
                aus_fcronhasta = datetime.datetime.strptime(campos[10], "%d/%m/%Y").date()                
            aus_diascaidos = campos[11].strip()
            if campos[11]=='':
                aus_diascaidos = None
            aus_diasjustif = campos[12].strip()
            if campos[12]=='':
                aus_diasjustif = None
            if campos[13]=='':
                aus_freintegro = None
            else:
                aus_freintegro = datetime.datetime.strptime(campos[13], "%d/%m/%Y").date()                
            
            if campos[14]=='':
                aus_falta = None
            else:
                aus_falta = datetime.datetime.strptime(campos[14], "%d/%m/%Y").date()                
            
            austa = campos[15].strip()
            if austa=='':
                aus_tipo_alta = None
            else:
                aus_tipo_alta=dict(TIPO_ALTA)        
                aus_tipo_alta = [k for k, v in aus_tipo_alta.items() if v == austa][0]

            if campos[16]=='':
                aus_frevision = None
            else:
                aus_frevision = datetime.datetime.strptime(campos[16], "%d/%m/%Y").date()                

            aus_medico = campos[17].strip().upper()
            if aus_medico=='':
                aus_medico=None
            else:
                aus_medico = ent_medico_prof.objects.get_or_create(apellido_y_nombre=aus_medico)[0]                           

            aus_grupop = campos[18].strip().upper()
            if aus_grupop=='':
                aus_grupop=None
            else:
                aus_grupop = aus_patologia.objects.get_or_create(patologia=aus_grupop)[0]       

            aus_diagn = campos[19].strip().upper()
            if aus_diagn=='':
                aus_diagn=None
            else:
                aus_diagn = aus_diagnostico.objects.get_or_create(diagnostico=aus_diagn)[0]              

                   
            observaciones = campos[20].strip()                
            descr_altaparc = campos[21].strip()                
            
            try:
               ausentismo.objects.update_or_create(empleado=empleado,tipo_ausentismo=tipoa,aus_control=aus_control,aus_fcontrol=aus_fcontrol,aus_certificado=aus_certificado,
                aus_fcertif=aus_fcertif,aus_fentrega_certif=aus_fentrega_certif,aus_fcrondesde=aus_fcrondesde,aus_fcronhasta=aus_fcronhasta,aus_diascaidos=aus_diascaidos,
                aus_diasjustif=aus_diasjustif,aus_freintegro=aus_freintegro,aus_falta=aus_falta,aus_tipo_alta=aus_tipo_alta,aus_frevision=aus_frevision,aus_medico=aus_medico,
                aus_grupop=aus_grupop,aus_diagn=aus_diagn,observaciones=observaciones,descr_altaparc=descr_altaparc)                                          
               print index
            except Exception as e:
                print e
                print dni                            

    return render(request, 'general/importar.html')