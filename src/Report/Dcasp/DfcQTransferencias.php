<?php

namespace RptGen\Report\Dcasp;

use DateTime;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use RptGen\Db;

/**
 * DCASP - DFC - Quadro das transferências recebidas e concedidas
 *
 * @author Everton
 */
final class DfcQTransferencias extends DcaspBase {

    public function __construct(Db $con, Spreadsheet $spreadsheet, int $remessa, string $escopo) {
        parent::__construct('DFC Q1', $con, $spreadsheet, $remessa, $escopo);
    }

    public function run(): void {
        printf("\t-> gerando planilha %s" . PHP_EOL, $this->sheetName);

        $sheet = $this->spreadsheet->setActiveSheetIndexByName($this->sheetName);

        foreach ($this->getCellMap() as $cellAddress => $cellValue) {
            $sheet->setCellValue($cellAddress, $cellValue);
        }
    }

    protected function getCellMap(): array {
        $ano = substr($this->remessa, 0, 4);
        $data_inicial = (date_create_from_format('Y-m-d', "$ano-01-01"))->format('Y-m-d');
        $data_final = $this->dataBase->format('Y-m-d');
        $ano_anterior = substr($this->getRemessaAnoAnterior(), 0, 4);
        $data_inicial_anterior = "$ano_anterior-01-01";
        $data_final_anterior = "$ano_anterior-12-31";
        return [
            
            // Transferências recebidas
            'C12' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '171%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '241%', "('normal', 'dedutora')"),
            'C13' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '172%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '242%', "('normal', 'dedutora')"),
            'C14' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '173%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '243%', "('normal', 'dedutora')"),
//            'C15' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '1%', "('intra')")
//                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '2%', "('intra')"),
            'C15' => 0.0,
            'C16' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '174%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '175%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '176%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '177%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '178%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '179%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '244%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '245%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '246%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '247%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->remessa, $this->entidades, '248%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '4511%')
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '4512201%')
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '4513%')
            ,
            
            // Transferências concedidas
            'C21' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__20%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__22%'),
            'C22' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__30%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__31%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__32%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__35%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__36%'),
            'C23' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__40%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__41%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__42%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__45%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__46%'),
            'C24' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__71%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__72%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__73%'),
//            'C25' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__91%'),
            'C25' => 0.0,
            'C26' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__50%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__60%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__70%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__76%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->remessa, $this->entidades, $data_inicial, $data_final, '__80%')
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '3511%')
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '3512201%')
                    + $this->readSql('dcasp/bp/BalVerSaldoAtual', $this->consolidado, $this->remessa, $this->entidades, '3513%')
            ,
            
            // Transferências recebidas
            'D12' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '171%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '241%', "('normal', 'dedutora')"),
            'D13' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '172%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '242%', "('normal', 'dedutora')"),
            'D14' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '173%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '243%', "('normal', 'dedutora')"),
            'D15' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '1%', "('intra')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '2%', "('intra')"),
            'D16' => $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '174%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '175%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '176%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '177%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '178%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '244%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '245%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '246%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '247%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bo/BalRecReceitaRealizadaPorNro', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '248%', "('normal', 'dedutora')")
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '4511%')
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '4512201%')
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '4513%')
            ,
            
            // Transferências concedidas
            'D21' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__20%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__22%'),
            'D22' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__30%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__31%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__32%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__35%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__36%'),
            'D23' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__40%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__41%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__42%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__45%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__46%'),
            'D24' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__71%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__72%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__73%'),
//            'D25' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__91%'),
            'D25' => 0.0,
            'D26' => $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__50%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__60%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__70%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__76%')
                    + $this->readSql('dcasp/dfc/PagamentosPorNdo', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, $data_inicial_anterior, $data_final_anterior, '__80%')
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '3511%')
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '3512201%')
                    + $this->readSql('dcasp/bp/BverEncSaldoAtual', $this->consolidado, $this->getRemessaAnoAnterior(), $this->entidades, '3513%')
            ,
        ];
    }
    
    private function getRemessaAnoAnterior(): int {
        return (int) (substr($this->remessa, 0, 4) - 1).'12';
    }
    
}
