#!/bin/bash
echo -e "\n=============================================================================="
echo -e "  🚀 SINTEZIUM V7: СИНХРОНИЗАЦИЯ С УДАЛЕННЫМ МОНОЛИТНЫМ УЗЛОМ"
echo -e "==============================================================================\n"

REMOTE_NODE="sintezium-monolith-node"

echo "[1/4] Проверка подключения SSH к удаленному узлу $REMOTE_NODE..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_NODE" "echo '  - SSH Соединение установлено!'" || {
    echo "  [FAIL] Не удалось подключиться к $REMOTE_NODE";
    exit 1;
}

echo -e "\n[2/4] Создание директорий /opt/sintezium/{core,logs,knowledge,maps}..."
ssh "$REMOTE_NODE" "mkdir -p /opt/sintezium/core /opt/sintezium/logs /opt/sintezium/knowledge /opt/sintezium/maps"

echo -e "\n[3/4] Копирование ядра /opt/sintezium/core/ на $REMOTE_NODE..."
rsync -avz -e "ssh -o StrictHostKeyChecking=no" /opt/sintezium/core/ "$REMOTE_NODE":/opt/sintezium/core/
rsync -avz -e "ssh -o StrictHostKeyChecking=no" /opt/sintezium/knowledge/ "$REMOTE_NODE":/opt/sintezium/knowledge/ 2>/dev/null || true

echo -e "\n[4/4] Установка зависимостей Python на $REMOTE_NODE..."
ssh "$REMOTE_NODE" "pip3 install web3 python-dotenv bs4 requests eth-account --quiet"

echo -e "\n=============================================================================="
echo -e "  📌 СИНХРОНИЗАЦИЯ УСПЕШНО ЗАВЕРШЕНА!"
echo -e "==============================================================================\n"
