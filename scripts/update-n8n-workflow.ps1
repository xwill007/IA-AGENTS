param(
    [Parameter(Mandatory=$true)]
    [string]$WorkflowFile
)

# Lee el contenido del archivo JSON del workflow
$workflowContent = Get-Content -Path $WorkflowFile -Raw

# URL de la API de n8n
$n8nUrl = "http://localhost:5678/api/v1/workflows"

# Función para leer valores del archivo .env
function Get-EnvValue {
    param (
        [string]$key
    )
    $envContent = Get-Content "$PSScriptRoot\..\\.env"
    $value = $envContent | Where-Object { $_ -match "^$key=" } | ForEach-Object { $_.Split('=')[1] }
    return $value
}

# Obtener credenciales de n8n del archivo .env
$username = Get-EnvValue "N8N_BASIC_AUTH_USER"
$password = Get-EnvValue "N8N_BASIC_AUTH_PASSWORD"

# Obtener API key del archivo .env
$apiKey = Get-EnvValue "N8N_API_KEY"

# Configurar los headers con el API key
$headers = @{
    "X-N8N-Skip-WebhookAppend" = "true"
    "X-N8N-API-KEY" = $apiKey
}

# Obtén la lista de workflows existentes
$existingWorkflows = Invoke-RestMethod -Uri $n8nUrl -Method GET -Headers $headers

# Convierte el contenido del workflow a un objeto PowerShell
$workflow = $workflowContent | ConvertFrom-Json

# Busca si ya existe un workflow con el mismo nombre
$existingWorkflows = Invoke-RestMethod -Uri $n8nUrl -Method GET -Headers $headers
$existingWorkflow = $existingWorkflows.data | Where-Object { $_.name -eq $workflow.name }

if ($existingWorkflow) {
    Write-Host "Actualizando workflow existente: $($workflow.name)"
    $updateUrl = "$n8nUrl/$($existingWorkflow.id)"
    
    # Preparar el cuerpo de la solicitud
    $requestBody = @{
        name = $workflow.name
        nodes = $workflow.nodes
        connections = $workflow.connections
        settings = $workflow.settings
    }
    
    # Actualiza el workflow
    $response = Invoke-RestMethod -Uri $updateUrl -Method PUT -Body ($requestBody | ConvertTo-Json -Depth 100) -ContentType "application/json" -Headers $headers
    
    # Espera un momento para que los cambios se apliquen
    Start-Sleep -Seconds 2
    
    # Verifica el estado del workflow y actívalo si es necesario
    $workflowStatus = Invoke-RestMethod -Uri $updateUrl -Method GET -Headers $headers
    Write-Host "Estado actual del workflow: $(if ($workflowStatus.data.active) { 'Activo' } else { 'Inactivo' })"
    if (-not $workflowStatus.data.active) {
        Write-Host "Activando workflow..."
        $activateUrl = "$updateUrl/activate"
        try {
            $activateResponse = Invoke-RestMethod -Uri $activateUrl -Method POST -Headers $headers
            Write-Host "Workflow activado exitosamente"
        } catch {
            Write-Host "Error al activar el workflow: $_"
        }
    } else {
        Write-Host "El workflow ya está activo"
    }
} else {
    Write-Host "Creando nuevo workflow: $($workflow.name)"
    # Preparar el cuerpo de la solicitud
    $requestBody = @{
        name = $workflow.name
        nodes = $workflow.nodes
        connections = $workflow.connections
        settings = $workflow.settings
    }
    
    # Crea un nuevo workflow
    $response = Invoke-RestMethod -Uri $n8nUrl -Method POST -Body ($requestBody | ConvertTo-Json -Depth 100) -ContentType "application/json" -Headers $headers
    
    # Activar el nuevo workflow
    Write-Host "Activando nuevo workflow..."
    $activateUrl = "$n8nUrl/$($response.data.id)/activate"
    try {
        $activateResponse = Invoke-RestMethod -Uri $activateUrl -Method POST -Headers $headers
        Write-Host "Workflow activado exitosamente"
    } catch {
        Write-Host "Error al activar el workflow: $_"
    }
}

# Obtener la información final del workflow
$finalWorkflow = if ($existingWorkflow) {
    $workflowStatus.data
} else {
    $response.data
}

Write-Host "Finaliza actualizacion de: $($workflow.name)"
Write-Host "ID: $($finalWorkflow.id)"
Write-Host "Nombre: $($finalWorkflow.name)"
Write-Host "Estado: $(if ($finalWorkflow.active) { 'Activo' } else { 'Inactivo' })"
