#!/bin/bash
# Usage: ./create-fake-pedidos.sh "API_GATEWAY" "NUMBER_PEDIDOS"
# Ex.: ./create-fake-pedidos.sh "localhost:5000" 50
#      ./create-fake-pedidos.sh "35.198.3.94" 300

API_GATEWAY=${1}
NUMBER_PEDIDOS=${2}

# Create 100 pedidos
for i in $(seq 1 $NUMBER_PEDIDOS); do
    cliente="$((1 + ($RANDOM % 200)))"
    destinatario="$((1 + ($RANDOM % 200)))"
    prazo_pedido="$((5 + ($RANDOM % 15)))"
    valor_pedido="$(($RANDOM % 200)).$(($RANDOM%99))"

    # Create pedido
    pedido=$(curl -s --location --request POST "http://${API_GATEWAY}/pedidos" \
    --form "id_cliente=\"${cliente}\"" \
    --form "id_destinatario=\"${destinatario}\"" \
    --form "prazo_pedido=\"${prazo_pedido}\"" \
    --form "valor_pedido=\"${valor_pedido}\"")
    pedido_id=$(jq -r  '.id' <<< "${pedido}")
    
    echo "Pedido criado: ${pedido_id}"

    # Complete random N workitems
    completes=$(($RANDOM % 20))
    for j in $(seq 1 $completes); do
        curl -s --location --request PUT "http://${API_GATEWAY}/pedidos/${pedido_id}/workitems/0/complete"
    done
done
