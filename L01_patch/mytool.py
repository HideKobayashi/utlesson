from typing import Optional


def add(a: int, b: int) -> int:
    """二つの正の整数を加算する

    Args:
        a (int): 一つ目の正の整数
        b (int): 二つ目の正の整数

    Raises:
        RuntimeError: 与えられた二数のいずれか正の整数でないときに上がる例外

    Returns:
        int: 二数の輪
    """
    if a < 1 or b < 1:
        raise RuntimeError(
            f"Given argunents a and b must be positive integers. (a, b)=({a}, {b})"
        )
    return a + b


def log_print(level: str, message: str) -> None:
    """ログを表示する

    Args:
        level (str): ログレベル
        message (str): ログメッセージ
    """
    log_info = f"{level} {message}"
    print("log:", log_info)


def main(a: int, b: int) -> Optional[int]:
    """メイン関数

    Args:
        a (int): 一つ目の整数
        b (int): 二つ目の整数

    Returns:
        Optional[int]: 二数の輪
    """
    result = None
    try:
        result = add(a, b)
        log_print("INFO", "Success")
    except RuntimeError as e:
        log_print("WARNING", f"RuntimeError info: {e.args[0]}")
    except Exception as e:
        log_print("ERROR", f"Exception info: {e.args[0]}")
    return result
