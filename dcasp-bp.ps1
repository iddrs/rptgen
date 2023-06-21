#Ponto de entrada para o Balanço Patrimonial

#$periodo = 0
#$ano = Read-Host "Digite o ano [AAAA]"
#do {
#    $mes = Read-Host "Digite o mês [1 ~ 12]"
#    if ($mes -ge 1 -and $mes -le 12) {
#        $periodo = 1
#    } else {
#        Write-Error "O mês deve estar entre 1 e 12!"
#    }
#} while($periodo -eq 0)
#
#$opt = '&Câmara', '&FPSM', '&Prefeitura', '&Município (Consolidado)'
#$escopo = $Host.UI.PromptForChoice('Selecionando o escopo do relatório', 'Escolha um escopo:', $opt, -1)
#if ($escopo -eq 0) {
#    $nome_escopo = 'Câmara'
#} elseif ($escopo -eq 1) {
#    $nome_escopo = 'FPSM'
#} elseif ($escopo -eq 2) {
#    $nome_escopo = 'Prefeitura'
#} elseif ($escopo -eq 3) {
#    $nome_escopo = 'Município (Consolidado)'
#} else {
#    Write-Error 'Escopo inválido!'
#    exit
#}
#
#
#$opt = '&Preparar os dados', 'Gerar relatório em &HTML', 'Gerar relatório em &PDF'
#$acao = $Host.UI.PromptForChoice('Selecionando a ação desejada', 'Escolha uma ação:', $opt, -1)
#if ($acao -eq 0) {
#    $nome_acao = 'Preparar dados'
#} elseif ($acao -eq 1) {
#    $nome_acao = 'Gerar relatório em HTML'
#} elseif ($acao -eq 2) {
#    $nome_acao = 'Gerar relatório em PDF'
#} else {
#    Write-Error 'Ação inválida!'
#    exit
#}
#
#Write-Host "====================================================="
#Write-Host "Resumo:"
#Write-Host "====================================================="
#
#Write-Host "Período         $($mes)\$($ano)"
#Write-Host "Escopo          $($nome_escopo)"
#Write-Host "Ação            $($nome_acao)"

# para testes
$ano = 2022
$mes = 12
$escopo = 2
$acao = 1
# para testes

if ($acao -eq 0)
{
    cd dcasp
    python 'bp-etl.py' --ano $ano --mes $mes --escopo $escopo
}elseif ($acao -eq 1) {
    cd dcasp
    python 'bp-ohtml.py' --ano $ano --mes $mes --escopo $escopo
} else {
    Write-Error "Ação não reconhecida!"
}

cd ..