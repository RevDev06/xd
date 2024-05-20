

email_sender = EmailSender('pruebaautomatizacionemails@gmail.com', 'hquw jsca rrym lwas')
email_sender.send_email(
    'danyjr@outlook.es', 
    'Prueba con adjunto', 
    'Que bueno soy\nPD. El correo se envio con un archivo adjunto', 
    attachments=['RH_pruebas/rh3.sql']
)
