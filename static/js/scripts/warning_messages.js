{% load i18n %}

{% if messages %}
    {% if message.tags == "warning" %}
        alerta = alertify.dialog('confirm').set({
            'labels': {
                ok: 'Aceptar',
                cancel: 'Cancelar'
            },
            'message': '¿Desea Eliminar los Ausentismos seleccionados?',
            transition: 'fade',
            'onok': function() {
                $.ajax({
                    url: "{{ action }}?ignorewarnings=true",
                    type: "post",
                    dataType: 'json',
                    success: function(data) {
                        window.location.href = window.location.href
                    }
                });
            },
            'oncancel': function() {
                return true;
            }
        });
        alerta.setting('modal', true);
        alerta.setHeader('ELIMINAR AUSENTISMOS');
        alerta.show();
        return true;
    {% endif %}
{% endif %}


{% if messages %}
	jQuery('#modalbox #modalbox_submit').show();
	jQuery('#modalbox #modalbox_cancel').show();
	jQuery('#modalbox #modalbox_ok').hide();

    var messages = 0;
    // Modalwindow Initialization
    ModalBox.init(// Previous defined action of the form, ModalBox will change the action of
                  // the form to this if the user clicks Cancel button.
                  $("{{ form_id }}"),
                  // This will be the action of the forms if we have warning messages.
                  "{{ action }}?ignorewarnings=true");

    // Loading Warning Messages in the Modal Window
    {% for message in messages %}
        {% if message.tags == "warning" %}
            ModalBox.addMessage("{{ message|escapejs|safe }}");
            messages += 1;
        {% endif %}
        {% if message.tags == "error" %}
            ModalBox.addMessage("{{ message|escapejs|safe }}");
            {# If error messages are present, hide default buttons and just show OK #}
            jQuery('#modalbox #modalbox_submit').hide();
            jQuery('#modalbox #modalbox_cancel').hide();
            jQuery('#modalbox #modalbox_ok').show();
            messages += 1;
        {% endif %}
    {% endfor %}

    // Showing Modal Window only if there's been any warning or error msg
    if(messages > 0)
        ModalBox.show();

    if ($('{{ form_id }}').length > 0)
		$('.ui-dialog button[title="Close"],.ui-dialog input[value="Cancel"]').click(function(){
			// Removing ignore warnings when clicking on cancel or close button
			var formAction = $('{{ form_id }}').prop('action');

			formAction = formAction.replace('?ignorewarnings=true', '');
			$('{{ form_id }}').prop('action', formAction);
		});
{% endif %}
