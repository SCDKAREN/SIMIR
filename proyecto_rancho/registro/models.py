from django.db import models
    
class Casino(models.Model): 
    nombre = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f" {self.nombre}"
    
class Comida(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f" {self.nombre}"
    
class Registro(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)  # Fecha y hora del registro (se guarda automáticamente)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=50)
    casino = models.ForeignKey(Casino, on_delete=models.CASCADE,  related_name='registros')
    confirmado = models.BooleanField(default=False)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE,  related_name='registros',null = True)
    
    def to_json(self):
        return {
            "id": self.id,
            "fecha_hora": self.fecha_hora.isoformat(),
            "apellido": self.apellido,
            "nombre": self.nombre,
            "documento": self.documento,
            "casino": self.casino.nombre if self.casino else None,
            "comida": self.comida.nombre if self.comida else None,
        }
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.documento}"