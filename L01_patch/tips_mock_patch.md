# unittest で mock で patch する方法

ここでは、関数が三つ定義された下記の実装を例として、mock オブジェクトで　 patch を行う方法を説明します。
例では、

- add
- log_print
- main

という三つの関数が定義され、main 関数の中で　 add と　 log_print を呼び出しているという構造になっているものとします。
add 関数では例外が発生する可能性があり、main 関数内で例外をキャッチして例外の種類（RuntimeError またはそれ以外）に応じて異なるログメッセージを記録するものとします。

実装例を下記に示します。

```python
from typing import Optional
import traceback


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
    except Exception:
        log_print("ERROR", traceback.format_exc())
    return result
```

以下では、main 関数内で呼び出す add と log_print に対して patch を使うことを例として説明します。

## 1. 関数が呼ばれたときの引数の値を確認する方法

add 関数の処理が正常におわったときにログに "INFO" を書き込むように実装されていることを確認してみます。

下記の例では、log_print 関数を mock で patch して、mock オブジェクトを mock_log_print に代入しています。
位置引数のタプルを args という変数に入れて、位置引数の１番目が　"INFO" という文字列になっているかを確認します。

```python
class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_01_main_ok(self):
        """main関数の正常形 - (log_print を mock で patch して、ログレベルを確認)

        条件: a,b いずれも正の整数 (例 a=1, b=2)、add の戻り値がある (例 戻り値 3)
        期待値: mainの戻り値がaddの戻り値と同じ (例 戻り値 3), ログレベル "INFO"
        """
        a, b = 1, 2
        expect = 3
        expect_log_level = "INFO"

        # ログ出力関数を mock で patch
        with patch("mytool.log_print") as mock_log_print:
            result = main(a, b)

        # main の戻り値を確認
        self.assertEqual(result, expect)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        self.assertEqual(args[0], expect_log_level)

```

mock オブジェクトは、さまざまな属性を持っていますが、その中の一つに call_args というものがあります。
call_args は二つの要素をもつタプルになっており、一つ目の要素がタプル、二つ目の要素が辞書です。
一つ目の要素は、log_print 関数が呼ばれるときに与えられる位置引数のタプル、
二つ目の要素は、log_print 関数が呼ばれるときに与えられるキーワード引数の辞書になっています。

## 2. 関数をモックで置き換えて戻り値を任意の値に設定する方法

関数をモックで置き換えて戻り値に任意の値を設定するには、patch の引数に return_value を設定します。

下記の例では、は add を　 mock で patch して、return_value に任意の値を設定しています。
実際には、add に a=1, b=2 を代入すると 戻り値は 3 になりますが、mock した関数の戻り値を 30 にすると add が実行されたときの戻り値を 30 にすることができます。このとき main 関数の戻り値の期待値は 30 です。

```python
class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_02_main_ok_mock(self):
        """main関数の正常形 - (addをmockでpatch)

        条件: a,b いずれも整数 (add が mock なので任意)、add の戻り値がある (例 戻り値 3)
        期待値: mainの戻り値がaddの戻り値と同じ (例 戻り値 3)、ログレベル "INFO"
        """
        a, b = 1, 2
        mock_return = 30  # 任意の値
        # 期待値
        expect = mock_return

        # add関数を mock で patch
        with patch("mytool.add", return_value=mock_return) as mock_add:
            result = main(a, b)

        # add が呼ばれるときの引数を確認
        args, _kwargs = mock_add.call_args
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # main の戻り値を確認
        self.assertEqual(result, expect)
```

## 3. 二つの関数をモックで置き換える方法

add と log_print の両方をモックで置き換えるには with 文を入れ子にします。

```python
class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_02_main_ok_mock_log(self):
        """main関数の正常形 - (addをmockでpatch)

        条件: a,b いずれも整数 (add が mock なので任意)、add の戻り値がある (例 戻り値 3)
        期待値: mainの戻り値がaddの戻り値と同じ (例 戻り値 3)、ログレベル "INFO"
        """
        a, b = 1, 2
        mock_return = 3
        # 期待値
        expect = mock_return
        expect_log_level = "INFO"

        # add関数を mock で patch
        with patch("mytool.add", return_value=mock_return) as mock_add:
            # ログ出力関数を mock で patch
            with patch("mytool.log_print") as mock_log_print:
                result = main(a, b)

        # add が呼ばれるときの引数を確認
        args, _kwargs = mock_add.call_args
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # main の戻り値を確認
        self.assertEqual(result, expect)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        self.assertEqual(args[0], expect_log_level)
```

## 4. 関数をモックで置き換えて例外を発生させる方法

関数をモックで置き換えて例外を発生させるには、patch の引数 side_effect に 例外クラスまたは例外インスタンスを設定します。

add で RuntimeError 例外を発生させるには、patch の引数 side_effect に指定します。
期待値は log_print に渡される引数の期待値は、"WARNING" と "RuntimeError info:"が含まれる文字列、の二つです。

```python
class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_04_main_ng_warning_mock_log(self):
        """main関数の異常形 - add で RuntimeError 例外が上がる場合 (addをmockでpatch)

        条件: a, b いずれも整数 (addがmockなので任意)、関数 add で例外 RuntimeError が上がる
        期待値: main でキャッチして、ログレベル "WARNING"、ログメッセージ "RuntimeError info:"
        """
        a, b = 1, 2
        mock_side_eff = RuntimeError("テスト例外")
        # 期待値
        expect_log_level = "WARNING"
        expect_log_msg = "RuntimeError info:"

        # add関数を mock で patch
        with patch("mytool.add", side_effect=mock_side_eff) as mock_add:
            # ログ出力関数を mock で patch
            with patch("mytool.log_print") as mock_log_print:
                main(a, b)

        # add が呼ばれるときの引数を確認
        args, _kwargs = mock_add.call_args
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        self.assertEqual(args[0], expect_log_level)
        self.assertIn(expect_log_msg, args[1])
```

発生させる例外の種類を任意に切り替えることも可能です。
RuntimeError 以外の例外は発生する時の期待値は、"ERROR"、"Traceback"が含まれる文字列、の二つになります。

```python
class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_05_main_ng_error_mock(self):
        """main関数の異常形 - add で RuntimeError 以外の例外が上がる場合 (addをmockでpatch)

        条件: a, b いずれも整数 (addがmockなので任意)、関数 add で RuntimeError 以外の例外が上がる
        期待値: 、main でキャッチして、ログレベル "ERROR"、ログメッセージ "Traceback"
        """
        a, b = 1, 2
        # mock_side_eff に RuntimeError 以外で Exception を継承する任意の例外を設定
        # mock_side_eff = TypeError("テスト例外")
        # mock_side_eff = OSError("テスト例外")
        # mock_side_eff = ValueError("テスト例外")
        mock_side_eff = Exception("テスト例外")
        # 期待値
        expect_log_level = "ERROR"
        expect_log_msg = "Traceback"

        # add関数を mock で patch
        with patch("mytool.add", side_effect=mock_side_eff) as mock_add:
            # ログ出力関数を mock で patch
            with patch("mytool.log_print") as mock_log_print:
                main(a, b)

        # add が呼ばれるときの引数を確認
        args, _kwargs = mock_add.call_args
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        self.assertEqual(args[0], expect_log_level)
        self.assertIn(expect_log_msg, args[1])
```
