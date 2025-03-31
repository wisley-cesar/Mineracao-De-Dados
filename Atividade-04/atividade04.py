import sqlite3
from tabulate import tabulate

# Conectar ao banco de dados
conn = sqlite3.connect("shopping.sqlite")
cursor = conn.cursor()

# Abrir um arquivo para salvar os resultados
with open("resultado.txt", "w", encoding="utf-8") as file:
    
    # 1️⃣ Total de compras registradas
    cursor.execute("SELECT COUNT(*) FROM customer_shopping_data;")
    total_compras = cursor.fetchone()[0]
    total_compras_text = f"\n🛒 Total de compras registradas: {total_compras}\n"
    print(total_compras_text)
    file.write(total_compras_text)

    # 2️⃣ Média de preço por categoria
    cursor.execute("SELECT category, AVG(price) FROM customer_shopping_data GROUP BY category;")
    media_precos = cursor.fetchall()
    media_precos_text = "\n📊 Média de preço por categoria:\n" + tabulate(media_precos, headers=["Categoria", "Preço Médio"], tablefmt="fancy_grid") + "\n"
    print(media_precos_text)
    file.write(media_precos_text)

    # 3️⃣ Quantidade de compras por método de pagamento
    cursor.execute("SELECT payment_method, COUNT(*) FROM customer_shopping_data GROUP BY payment_method;")
    compras_pagamento = cursor.fetchall()
    compras_pagamento_text = "\n💳 Quantidade de compras por método de pagamento:\n" + tabulate(compras_pagamento, headers=["Método de Pagamento", "Quantidade"], tablefmt="fancy_grid") + "\n"
    print(compras_pagamento_text)
    file.write(compras_pagamento_text)

    # 4️⃣ Cliente que mais gastou
    cursor.execute("SELECT customer_id, SUM(price * quantity) as total_gasto FROM customer_shopping_data GROUP BY customer_id ORDER BY total_gasto DESC LIMIT 1;")
    top_cliente = cursor.fetchone()
    top_cliente_text = f"\n🏆 Cliente que mais gastou:\nCliente: {top_cliente[0]}\nTotal gasto: R$ {top_cliente[1]:.2f}\n"
    print(top_cliente_text)
    file.write(top_cliente_text)

# Fechar a conexão
conn.close()

print("\n✅ Os resultados foram salvos no arquivo 'resultado.txt'!")
