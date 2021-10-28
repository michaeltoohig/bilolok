async def test_arq_subtask(ctx: dict, letter: str):
    return f"test sub task return {letter}"


async def test_arq(ctx: dict, word: str):
    arq_app = ctx["redis"]
    for i, letter in enumerate(word):
        await arq_app.enqueue_job("test_arq_subtask", letter, _defer_by=1)
    return f"test task return {word}"
