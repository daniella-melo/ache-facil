from django.db import models

class Local(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nome

class Cor(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome

class Objeto(models.Model):
    STATUS_CHOICES = (
        ('ACHADO', 'Objeto Achado (Devolvido)'),
        ('PERDIDO', 'Objeto Perdido (Buscando Dono)'),
    )

    nome = models.CharField(max_length=255)
    local_encontrado = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True)   
    data_cadastro = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='objetos_encontrados/', null=True, blank=True)
    cor = models.ForeignKey(Cor, on_delete=models.SET_NULL, null=True, verbose_name="Cor Principal")
    
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PERDIDO'
    )  

    def __str__(self):
        return f'{self.nome} ({self.get_status_display()})'

    class Meta:
        ordering = ['-data_cadastro']