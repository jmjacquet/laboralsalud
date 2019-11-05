# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.conf import settings
from general.views import VariablesMixin
# from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.utils.decorators import method_decorator
from .forms import AusentismoForm,PatologiaForm,DiagnosticoForm,ConsultaAusentismos
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId,usuario_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.db.models import Q,Sum,Count,FloatField,Func


############ AUSENTISMOS ############################

class AusentismoView(VariablesMixin,ListView):
    model = ausentismo
    template_name = 'ausentismos/ausentismo_listado.html'
    context_object_name = 'ausentismos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(AusentismoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoView, self).get_context_data(**kwargs)

        form = ConsultaAusentismos(self.request.POST or None,request=self.request)   
        ausentismos = ausentismo.objects.filter(baja=False,empleado__empresa__pk__in=empresas_habilitadas(self.request))[:20]
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            estado = form.cleaned_data['estado']
          
            ausentismos = ausentismo.objects.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

            if int(estado) == 0:  
                ausentismos = ausentismos.filter(baja=False)
            if fdesde:                
                ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))                         
            if fhasta:                
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))                                
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(empleado__apellido_y_nombre__icontains=empleado)
            if int(tipo_ausentismo) > 0: 
                ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))            
                
        context['form'] = form
        context['ausentismos'] = ausentismos.select_related('empleado','empleado__art','empleado__empresa','aus_grupop','aus_diagn')
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

class AusentismoCreateView(VariablesMixin,CreateView):
    form_class = AusentismoForm
    template_name = 'ausentismos/ausentismo_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
        return super(AusentismoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        form.instance.usuario = usuario_actual(self.request)        
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
        return super(AusentismoCreateView, self).form_invalid(form)

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
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(AusentismoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(AusentismoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(AusentismoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(AusentismoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(AusentismoEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'
        return initial  

    def get_success_url(self):        
        return reverse('ausentismo_listado')          


class AusentismoVerView(VariablesMixin,DetailView):
    model = ausentismo
    pk_url_kwarg = 'id'
    context_object_name = 'a'
    template_name = 'ausentismos/ausentismo_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(AusentismoVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def ausentismo_baja_alta(request,id):
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
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(PatologiaView, self).dispatch(*args, **kwargs)
    

class PatologiaCreateView(VariablesMixin,AjaxCreateView):
    form_class = PatologiaForm
    template_name = 'fm/entidades/form_patologia.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
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
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
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
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(DiagnosticoView, self).dispatch(*args, **kwargs)
    

class DiagnosticoCreateView(VariablesMixin,AjaxCreateView):
    form_class = DiagnosticoForm
    template_name = 'fm/entidades/form_diagnostico.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
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
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
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
   

def ausencias_importar(request):
    data = {}    
   
    # if request.method == 'POST':  
    #     csv_file = request.FILES["archivo"]
    #     #tabla = request.POST['username']     
    #     if not csv_file.name.endswith('.csv'):
    #         messages.error(request,'File is not CSV type')
    #         return HttpResponseRedirect(reverse("simple_upload"))
    #     #if file is too large, return
    #     if csv_file.multiple_chunks():
    #         messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
    #         return HttpResponseRedirect(reverse("simple_upload"))

    #     file_data = csv_file.read().decode("utf8", "ignore")

    #     lines = file_data.split("\n")
    #     cant = len(lines)
    #     try:
    #         for index,line in enumerate(lines):                      
    #             campos = line.split(";")
    #             legajo = campos[0].strip()                
    #             dni = campos[1].strip()                
    #             empleado = ent_empleado.objects.get(nro_doc=dni)            
    #             fecha_creacion = datetime.datetime.strptime(campos[2], "%d/%m/%Y").date()                
    #             tipoa = campos[3].strip()       
    #             #TIPO_AUSENCIA
    #             acontrol = campos[4].strip() == 'Si'
    #             fecha_control = datetime.datetime.strptime(campos[5], "%d/%m/%Y").date()                
    #             certificado = campos[6].strip() == 'Si'
    #             fecha_certif = datetime.datetime.strptime(campos[7], "%d/%m/%Y").date()                
    #             fecha_entrcertif = datetime.datetime.strptime(campos[8], "%d/%m/%Y").date()                
    #             aus_cron_desde = datetime.datetime.strptime(campos[9], "%d/%m/%Y").date()                
    #             aus_cron_hasta = datetime.datetime.strptime(campos[10], "%d/%m/%Y").date()                
    #             aus_diascaidos = campos[11].strip()
    #             aus_diasjustif = campos[12].strip()
    #             aus_freintegro = datetime.datetime.strptime(campos[13], "%d/%m/%Y").date()                
    #             aus_falta = datetime.datetime.strptime(campos[14], "%d/%m/%Y").date()                
    #             aus_tipo_alta = campos[15].strip()
    #             aus_frevision = datetime.datetime.strptime(campos[16], "%d/%m/%Y").date()                

    #             aus_medico = campos[17].strip().upper()
    #             if aus_medico=='':
    #                 aus_medico=None
    #             else:
    #                 aus_medico = ent_medico_prof.objects.get_or_create(apellido_y_nombre=aus_medico)                    

    #             art = ent_art.objects.get(nombre=art.strip())         
    #             empresa = campos[6]                
    #             empresa = ent_empresa.objects.get(razon_social=empresa.strip())
    #             puesto = campos[7]                
    #             puesto = ent_cargo.objects.get(cargo=puesto.strip())
                
    #             try:
    #                #ent_cargo.objects.update_or_create(cargo=cargo)                                                             
    #                try:
    #                    empl = ent_empresa.objects.get(nro_doc=dni.strip())
    #                except: 
    #                    ent_empleado.objects.update_or_create(nro_doc=dni,legajo=legajo,apellido_y_nombre=nombre,fecha_nac=fecha_nac,art=art,empresa=empresa,trab_cargo=puesto)                                          
    #                    print index
    #             except Exception as e:
    #                 print e
    #                 print nombre                    
    #             pass
    #     except Exception as e:
    #         print e
    #         print nombre

    return render(request, 'entidades/import.html')