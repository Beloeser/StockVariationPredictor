def calcular_estatisticas(df, dias):
    # Filtra só linhas com Close real
    df = df[df['Close'].notna()].copy()

    col_real = f'variacao_{dias}d_acao'
    col_pred = f'variacao_{dias}d_modelo'
    col_resultado = f'acertou_tendencia_{dias}d'

    df[col_real] = df['Close'].pct_change(periods=dias)
    df[col_pred] = df['predicoes'].pct_change(periods=dias)
    df = df.dropna(subset=[col_real, col_pred])
    df.loc[:, col_resultado] = (df[col_real] > 0) == (df[col_pred] > 0)
    df.loc[:, f'{col_real}_abs'] = df[col_real].abs()

    taxa_acerto = df[col_resultado].mean()
    taxa_erro = 1 - taxa_acerto
    media_lucro = df.groupby(col_resultado)[f'{col_real}_abs'].mean()
    lucro_acerto = media_lucro.get(True, 0)
    lucro_erro = media_lucro.get(False, 0)
    exp_mat_lucro = taxa_acerto * lucro_acerto - taxa_erro * lucro_erro
    ganho_sobre_perda = lucro_acerto / lucro_erro if lucro_erro != 0 else float('inf')

    #Remover isso antes do final, já que é só para teste/debug
    print(f"------ Precisão de {dias} DIAS ------")
    print(f"Média de lucro (acertou=False, acertou=True):")
    print(media_lucro)
    print(f"Ganho sobre perda: {ganho_sobre_perda:.2f}")
    print(f"Taxa de acerto ({dias}d): {taxa_acerto:.2%}")
    print(f"Expectativa matemática de lucro ({dias}d): {exp_mat_lucro:.4f}")
    print()

    return {
        "dias": dias,
        "taxa_acerto": taxa_acerto,
        "lucro_acerto": lucro_acerto,
        "lucro_erro": lucro_erro,
        "exp_mat_lucro": exp_mat_lucro,
        "ganho_sobre_perda": ganho_sobre_perda
    }