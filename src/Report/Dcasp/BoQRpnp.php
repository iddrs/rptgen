<?php

namespace RptGen\Report\Dcasp;

use DateTime;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use RptGen\Db;

/**
 * DCASP - Balanço Orçamentário - Quadro dos restos a pagar não processados
 *
 * @author Everton
 */
final class BoQRpnp extends DcaspBase {

    public function __construct(Db $con, Spreadsheet $spreadsheet, int $remessa, string $escopo) {
        parent::__construct('BO Q1', $con, $spreadsheet, $remessa, $escopo);
    }

    public function run(): void {
        printf("\t-> gerando planilha %s" . PHP_EOL, $this->sheetName);

        $sheet = $this->spreadsheet->setActiveSheetIndexByName($this->sheetName);

        foreach ($this->getCellMap() as $cellAddress => $cellValue) {
            $sheet->setCellValue($cellAddress, $cellValue);
        }
    }

    protected function getCellMap(): array {
        return [
            
            // Inscritos em exercícios anteriores
            'C14' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '31%'),
            'C15' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '32%'),
            'C16' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '33%'),
            'C19' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '44%'),
            'C20' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '45%'),
            'C21' => $this->readSql('dcasp/bo/RpPorNdo', 'saldo_nao_processado_inscritos_exercicios_anteriores', $this->consolidado, $this->remessa, $this->entidades, '46%'),
            
            // Inscritos no exercício anterior
            'D14' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '31%'),
            'D15' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '32%'),
            'D16' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '33%'),
            'D19' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '44%'),
            'D20' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '45%'),
            'D21' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_inscritos_ultimo_exercicio', $this->consolidado, $this->remessa, $this->entidades, '46%'),
            
            // Liquidados
            'E14' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '31%'),
            'E15' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '32%'),
            'E16' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '33%'),
            'E19' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '44%'),
            'E20' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '45%'),
            'E21' => $this->readSql('dcasp/bo/RpPorNdo', 'rp_liquidado', $this->consolidado, $this->remessa, $this->entidades, '46%'),
            
            // Pagos
            'F14' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '31%'),
            'F15' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '32%'),
            'F16' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '33%'),
            'F19' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '44%'),
            'F20' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '45%'),
            'F21' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_pago', $this->consolidado, $this->remessa, $this->entidades, '46%'),
            
            // Cancelado
            'G14' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '31%'),
            'G15' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '32%'),
            'G16' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '33%'),
            'G19' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '44%'),
            'G20' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '45%'),
            'G21' => $this->readSql('dcasp/bo/RpPorNdo', 'nao_processado_cancelado', $this->consolidado, $this->remessa, $this->entidades, '46%'),
            
            
            

        ];
    }
    
}
