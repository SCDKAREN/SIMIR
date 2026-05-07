from django.db import models
from django.conf import settings
from registro.models import Comida, Casino


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class DispositivoBiometrico(BaseModel):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    casino = models.ForeignKey(Casino, on_delete=models.PROTECT, related_name="dispositivos")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Dispositivo Biométrico"
        verbose_name_plural = "Dispositivos Biométricos"

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"


class UsuarioBiometrico(BaseModel):
    """Mapeo entre Usuario del sistema y user_id en el dispositivo."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfiles_biometricos",
    )
    dispositivo = models.ForeignKey(
        DispositivoBiometrico,
        on_delete=models.CASCADE,
        related_name="usuarios",
    )
    user_id_dispositivo = models.PositiveIntegerField()

    class Meta:
        unique_together = ("dispositivo", "user_id_dispositivo")
        verbose_name = "Usuario Biométrico"
        verbose_name_plural = "Usuarios Biométricos"

    def __str__(self):
        return f"{self.usuario} → {self.dispositivo} (uid={self.user_id_dispositivo})"


class LogBiometrico(BaseModel):
    """Registro crudo tal como llega desde el dispositivo, sin procesar."""
    dispositivo = models.ForeignKey(
        DispositivoBiometrico,
        on_delete=models.PROTECT,
        related_name="logs",
    )
    user_id_dispositivo = models.PositiveIntegerField(db_index=True)
    timestamp_dispositivo = models.DateTimeField(db_index=True)
    tipo_verificacion = models.PositiveSmallIntegerField(default=1)  # 1=huella, 4=tarjeta, etc.
    payload_raw = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["dispositivo", "timestamp_dispositivo"]),
        ]
        verbose_name = "Log Biométrico"
        verbose_name_plural = "Logs Biométricos"

    def __str__(self):
        return f"Log uid={self.user_id_dispositivo} @ {self.timestamp_dispositivo}"


class AsistenciaComida(BaseModel):
    """Asistencia confirmada a una comida, derivada de un log biométrico."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="asistencias",
    )
    comida = models.ForeignKey(Comida, on_delete=models.PROTECT, related_name="asistencias")
    casino = models.ForeignKey(Casino, on_delete=models.PROTECT, related_name="asistencias")
    log_origen = models.OneToOneField(
        LogBiometrico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asistencia",
    )
    fecha = models.DateField(db_index=True)

    class Meta:
        unique_together = ("usuario", "comida", "fecha")
        indexes = [
            models.Index(fields=["fecha", "comida"]),
            models.Index(fields=["casino", "fecha"]),
        ]
        verbose_name = "Asistencia a Comida"
        verbose_name_plural = "Asistencias a Comidas"

    def __str__(self):
        return f"{self.usuario} - {self.comida} ({self.fecha})"
