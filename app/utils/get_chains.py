def get_chains(game):
    chains = []

    if "tokens" not in game:
        return chains

    tokens = game['tokens']

    chain_names = ['bsc', 'eth', 'polygon']

    for chain_name in chain_names:
        if chain_name in tokens and len(tokens[chain_name]) and tokens[chain_name][0]:
            chains.append(chain_name)

    return chains
