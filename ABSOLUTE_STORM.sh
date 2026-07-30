#!/bin/bash
echo '========================================================================'
echo '        I G N I T I O N :   A B S O L U T E   S T O R M   (V7)          '
echo '========================================================================'
cd /opt/sintezium/core

echo -e '\n>>> [ФАЗА 1] ПРОБУЖДЕНИЕ ОРАКУЛОВ (TRADFI & CRYPTO) <<<'
python3 COINGECKO_PRICE_FEED.py
sleep 1
python3 NPB_FOREX_BRIDGE.py
sleep 1

echo -e '\n>>> [ФАЗА 2] ИИ-АНАЛИЗ КАРТ И ЛИТОСФЕРЫ (BEDROCK 87 / M-CAR) <<<'
# Run AI analyzer and wait for it to process
python3 MCAR_DISCOVERER_AGENT.py
sleep 2

echo -e '\n>>> [ФАЗА 3] СИНТЕЗ ИНТЕНТОВ (КОМПИЛЯТОР ЛАВЛЕЙС) <<<'
python3 LOVELACE_INTENT_COMPILER.py
sleep 2

echo -e '\n>>> [ФАЗА 4] ЭМИССИЯ ОБЕСПЕЧЕННЫХ ОБЛИГАЦИЙ (DEBT CAPITAL) <<<'
python3 RWA_BOND_ISSUER.py
sleep 2

echo -e '\n>>> [ФАЗА 5] АГРЕССИВНЫЙ БРОАДКАСТ В DARKPOOLS (ARBITRUM & POLYGON) <<<'
python3 GLOBAL_INTENT_BROADCASTER.py
sleep 1
python3 ARBITRUM_CROSSCHAIN_INTENT.py
sleep 1

echo -e '\n>>> [ФАЗА 6] ПЕРЕЗАГРУЗКА БЕССМЕРТНЫХ СЛУЖБ (SYSTEMD) <<<'
sudo systemctl restart solver_monitor.service
sudo systemctl restart pimlico_engine.service
sudo systemctl restart intent_accelerator.service

echo -e '\n========================================================================'
echo ' [✅ СТАТУС: АБСОЛЮТНАЯ ЭКСПАНСИЯ] Все сети накрыты ордерами Синтезиума! '
echo '========================================================================'
