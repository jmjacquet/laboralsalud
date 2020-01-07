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
from modal.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.db.models import Q,Sum,Count,FloatField,Func
from django.forms.models import inlineformset_factory,BaseInlineFormSet,formset_factory
from django.utils.functional import curry 

from .models import *
from entidades.models import ent_empleado
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
        ausentismos = ausentismos.filter(aus_fcrondesde__gte=fdesde,aus_fcronhasta__lte=fhasta)                                
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            estado = form.cleaned_data['estado']
          
            ausentismos = ausentismo.objects.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

            if int(estado) == 1:  
                ausentismos = ausentismos.filter(aus_fcronhasta__gte=hoy())
            elif int(estado) == 2:  
                ausentismos = ausentismos.filter(aus_fcronhasta__lt=hoy())
            elif int(estado) == 0: 
                ausentismos = ausentismos.filter(Q(aus_fcrondesde__range=[fdesde,fhasta])|Q(aus_fcronhasta__range=[fdesde,fhasta])
                |Q(aus_fcrondesde__lt=fdesde,aus_fcronhasta__gt=fhasta)) 
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
        context['ausentismos'] = ausentismos.select_related('empleado','empleado__empresa','aus_grupop','aus_diagn','usuario_carga')
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class ControlesDetalleFormSet(BaseInlineFormSet): 
    pass  
ControlDetalleFormSet = inlineformset_factory(ausentismo, ausentismo_controles,form=ControlesDetalleForm,formset=ControlesDetalleFormSet, can_delete=True,extra=0,min_num=10,max_num=13)

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
        self.object.usuario_carga = usuario_actual(self.request)             
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
            return self.form_invalid(form,controles_detalle)  

    def form_valid(self, form,controles_detalle):                                
        self.object.save()
        controles_detalle.instance = self.object
        controles_detalle.ausentismo = self.object.id        
        controles_detalle.usuario_carga = usuario_actual(self.request)        
        controles_detalle.save()   
        return HttpResponseRedirect(reverse('ausentismo_listado'))

    def form_invalid(self, form,controles_detalle):        
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

    def get_context_data(self, **kwargs):
        context = super(AusentismoVerView, self).get_context_data(**kwargs)
        a = self.get_object()
        context['controles'] = ausentismo_controles.objects.filter(ausentismo=a)
        return context

class AusentismoHistorialView(VariablesMixin,DetailView):
    model = ent_empleado
    pk_url_kwarg = 'id'
    context_object_name = 'empleado'
    template_name = 'ausentismos/historia_clinica.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(AusentismoHistorialView, self).dispatch(*args, **kwargs)        

    def get_context_data(self, **kwargs):
        context = super(AusentismoHistorialView, self).get_context_data(**kwargs)
        e = self.get_object()
        context['historial'] = ausentismo.objects.filter(empleado=e)
        return context


@login_required 
def ausentismo_eliminar(request,id):
    if not tiene_permiso(request,'aus_abm'):
            return redirect(reverse('principal'))
    aus = ausentismo.objects.get(pk=id).delete()         
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
    template_name = 'modal/entidades/form_patologia.html'

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
    template_name = 'modal/entidades/form_patologia.html'
    

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
    


@login_required 
def patologia_baja_alta(request,id):
    patologia = aus_patologia.objects.get(pk=id)     
    patologia.baja = not patologia.baja
    patologia.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("patologia_listado")) 


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
    template_name = 'modal/entidades/form_diagnostico.html'

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
    template_name = 'modal/entidades/form_diagnostico.html'
    

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

@login_required 
def diagnostico_baja_alta(request,id):
    diagnostico = aus_diagnostico.objects.get(pk=id)     
    diagnostico.baja = not diagnostico.baja
    diagnostico.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("diagnostico_listado")) 


import csv, io
from .forms import ImportarAusentismosForm   
from general.views import getVariablesMixin
import datetime
import random
@login_required 
def ausencias_importar(request):
    context = {}
    context = getVariablesMixin(request) 
    if request.method == 'POST':
        form = ImportarAusentismosForm(request.POST,request.FILES,request=request)
        if form.is_valid(): 
            csv_file = form.cleaned_data['archivo']
            empresa = form.cleaned_data['empresa']
            sobreescribir = form.cleaned_data['sobreescribir'] == 'S'
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'¡El archivo debe tener extensión .CSV!')
                return HttpResponseRedirect(reverse("importar_empleados"))
            
            if csv_file.multiple_chunks():
                messages.error(request,"El archivo es demasiado grande (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("importar_empleados"))

            decoded_file = csv_file.read().decode("utf8", "ignore").replace(",", "").replace("'", "")
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)            
            
            # DNI;TIPO_AUSENCIA;aus_control;aus_fcontrol;aus_certificado;aus_fcertif;aus_fentrega_certif;aus_fcrondesde;aus_fcronhasta;aus_diascaidos;
            # aus_diasjustif;aus_freintegro;aus_falta;TIPO_ALTA;aus_frevision;aus_medico;aus_grupop;aus_diagn;TIPO_ACCIDENTE;art_ndenuncia;art_faccidente;
            # art_fdenuncia;observaciones;descr_altaparc;detalle_acc_art;estudios_partic;estudios_art;recalificac_art
            cant=0
            # try:
            next(reader) #Omito el Encabezado                            
            for index,line in enumerate(reader):                      
              
                campos = line[0].split(";")                  
               
                dni = campos[0].strip()                
                if dni=='':
                    continue #Salta al siguiente                          

                try:
                    empl = ent_empleado.objects.get(nro_doc=dni)
                except:
                    messages.error(request,u'Empleado no existente! (%s)'%dni)   
                    continue
                if (empl.empresa==empresa) and not sobreescribir:
                    continue
                
                tipoa = campos[1].strip()                       
                if tipoa=='':
                    tipoa = None
                else:
                    ta=dict(TIPO_AUSENCIA)        
                    tipoa = [k for k, v in ta.items() if v.upper() == tipoa.upper()][0]

                if (campos[2].strip().upper() == 'SI'): 
                    aus_control = 'S' 
                else: 
                    aus_control = 'N'
                 
                if campos[3].strip()=='':
                    aus_fcontrol = None
                else:
                    aus_fcontrol = datetime.datetime.strptime(campos[3], "%d/%m/%Y").date()                

                if (campos[4].strip().upper() == 'SI'): 
                    aus_certificado = 'S' 
                else: 
                    aus_certificado = 'N'

                if campos[5]=='':
                    aus_fcertif = None
                else:
                    aus_fcertif = datetime.datetime.strptime(campos[5], "%d/%m/%Y").date()                
                if campos[6]=='':
                    aus_fentrega_certif = None
                else:
                    aus_fentrega_certif = datetime.datetime.strptime(campos[6], "%d/%m/%Y").date()                
                
                if campos[7]=='':
                    aus_fcrondesde = None
                else:
                    aus_fcrondesde = datetime.datetime.strptime(campos[7], "%d/%m/%Y").date()                
                if campos[8]=='':
                    aus_fcronhasta = None
                else:
                    aus_fcronhasta = datetime.datetime.strptime(campos[8], "%d/%m/%Y").date()                
                
                if campos[9]=='':
                    aus_diascaidos = None
                else:
                    aus_diascaidos = campos[9].strip()
                
                if campos[10]=='':
                    aus_diasjustif = None
                else:
                    aus_diasjustif = campos[10].strip()
                
                if campos[11]=='':
                    aus_freintegro = None
                else:
                    aus_freintegro = datetime.datetime.strptime(campos[11], "%d/%m/%Y").date()                
                
                if campos[12]=='':
                    aus_falta = None
                else:
                    aus_falta = datetime.datetime.strptime(campos[12], "%d/%m/%Y").date()                
                
                austa = campos[13].strip()
                if austa=='':
                    aus_tipo_alta = None
                else:
                    aus_tipo_alta=dict(TIPO_ALTA)        
                    aus_tipo_alta = [k for k, v in aus_tipo_alta.items() if v.upper() == austa.upper()][0]

                if campos[14]=='':
                    aus_frevision = None
                else:
                    aus_frevision = datetime.datetime.strptime(campos[14], "%d/%m/%Y").date()                

                aus_medico = campos[15].strip().upper()
              
                if aus_medico=='':
                    aus_medico=None
                else:
                    aus_medico = ent_medico_prof.objects.get_or_create(apellido_y_nombre=aus_medico)[0]                           

                aus_grupop = campos[16].strip().upper()
                if aus_grupop=='':
                    aus_grupop=None
                else:
                    aus_grupop = aus_patologia.objects.get_or_create(patologia=aus_grupop)[0]       

                aus_diagn = campos[17].strip().upper()
                if aus_diagn=='':
                    aus_diagn=None
                else:
                    aus_diagn = aus_diagnostico.objects.get_or_create(diagnostico=aus_diagn)[0]              

                tacc = campos[18].strip()
                if tacc=='':
                    art_tipo_accidente = None
                else:
                    art_tipo_accidente=dict(TIPO_ACCIDENTE)        
                    art_tipo_accidente = [k for k, v in art_tipo_accidente.items() if v.upper() == tacc.upper()][0]

                if campos[19]=='':
                    art_ndenuncia = None
                else:
                    art_ndenuncia = campos[19].strip()

                if campos[20]=='':
                    art_faccidente = None
                else:
                    art_faccidente = datetime.datetime.strptime(campos[20], "%d/%m/%Y").date()                

                if campos[21]=='':
                    art_fdenuncia = None
                else:
                    art_fdenuncia = datetime.datetime.strptime(campos[21], "%d/%m/%Y").date()    
                
                
               
                observaciones = campos[22].strip()                
                descr_altaparc = campos[23].strip()                
                detalle_acc_art = campos[24].strip()                
                estudios_partic = campos[25].strip()                
                estudios_art =campos[26].strip()                
                recalificac_art =campos[27].strip()                

        
                try:
                   ausentismo.objects.update_or_create(empleado=empl,tipo_ausentismo=tipoa,aus_control=aus_control,aus_fcontrol=aus_fcontrol,aus_certificado=aus_certificado,
                    aus_fcertif=aus_fcertif,aus_fentrega_certif=aus_fentrega_certif,aus_fcrondesde=aus_fcrondesde,aus_fcronhasta=aus_fcronhasta,aus_diascaidos=aus_diascaidos,
                    aus_diasjustif=aus_diasjustif,aus_freintegro=aus_freintegro,aus_falta=aus_falta,aus_tipo_alta=aus_tipo_alta,aus_frevision=aus_frevision,aus_medico=aus_medico,
                    aus_grupop=aus_grupop,aus_diagn=aus_diagn,art_tipo_accidente=art_tipo_accidente,art_ndenuncia=art_ndenuncia,art_faccidente=art_faccidente,art_fdenuncia=art_fdenuncia,
                    observaciones=observaciones,descr_altaparc=descr_altaparc,detalle_acc_art=detalle_acc_art,estudios_partic=estudios_partic,estudios_art=estudios_art,
                    recalificac_art=recalificac_art)                                                         
                   cant+=1
                except Exception as e:
                   error = u"Línea:%s -> %s" %(index,e)
                   messages.error(request,error)                                
            
            messages.success(request, u'Se importó el archivo con éxito!<br>(%s ausentismos creados/actualizados)'% cant )
            # except Exception as e:
            #     messages.error(request,u'Línea:%s -> %s' %(index,e))                        
    else:
        form = ImportarAusentismosForm(None,None,request=request)
    context['form'] = form    
    return render(request, 'ausentismos/importar_ausentismos.html',context)