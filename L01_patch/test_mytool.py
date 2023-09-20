from mytool import add, main
import unittest
from unittest.mock import patch


class TestAdd(unittest.TestCase):
    """add関数のテスト"""

    # 典型的な正常形のテスト
    # テストコードは、準備、実行、検証 の３段階を意識してブロックを分けて作成するとわかりやすい
    # 準備、実行、検証のコメントを略して、３つのブロックに分けるだけでもよい
    def test_01_add_ok(self):
        """add関数の正常形

        条件: a,b いずれも正の整数 (例 a=1, b=2)
        期待値: 戻り値がaとbの和 (例 戻り値 3)
        """
        # == 準備
        a, b = 1, 2
        expect = 3

        # == 実行
        result = add(a, b)

        # == 検証
        self.assertEqual(result, expect)

    # 例外が上がる異常形のテスト assertRases を使って例外が上がることを確認する
    # assertRases を使う時は、実行と検証が with文の中で行われる
    def test_02_add_ng(self):
        """add関数の異常形

        条件: a, b いずれかが正の整数でない (例 a=0, b=2)
        期待値: 例外 RuntimeError が上がる、
            例外メッセージ: "Given argunents a and b must be positive integers."
        """
        # == 準備
        a, b = 0, 2
        expect = RuntimeError
        expect_msg = "Given argunents a and b must be positive integers."

        # == 実行・検証
        with self.assertRaises(expect) as e:
            add(a, b)

        # == 検証
        # 例外情報の値に含まれる文字列を確認
        # print(e.exception.args[0])
        self.assertIn(expect_msg, e.exception.args[0])

    # 例外が上がる異常形のテスト assertRases を使って例外が上がることを確認する
    def test_02_add_ng_1(self):
        """add関数の異常形 - assertRasesの引数で例外メッセージを確認

        条件: a, b いずれかが正の整数でない (例 a=0, b=2)
        期待値: 例外 RuntimeError が上がる、
            例外メッセージ: "Given argunents a and b must be positive integers."
        """
        # == 準備
        a, b = 0, 2
        expect = RuntimeError
        expect_msg = "Given argunents a and b must be positive integers."

        # == 実行・検証
        with self.assertRaises(expect, msg=expect_msg):
            add(a, b)


class TestMain(unittest.TestCase):
    """main関数のテスト"""

    # mock.patch を使わない正常形のテスト
    # mainの正常形のテストを実施すると同時にaddの正常形もテストしていることになる
    def test_00_main_ok(self):
        """main関数の正常形

        条件: a,b いずれも正の整数 (例 a=1, b=2)、add の戻り値がaとbの和 (例 戻り値 3)
        期待値: mainの戻り値がaddの戻り値と同じ (例 戻り値 3)
        """
        a, b = 1, 2
        expect = 3

        result = main(a, b)

        # main の戻り値を確認
        self.assertEqual(result, expect)

    # log_print に mock.patch を使ったメイン関数の正常形のテスト
    # add が正常に戻り値を返すように a, b に妥当な値を与えている
    # patch の第一引数には、mock で置き換えたい関数のパスを文字列で指定する
    # log_print の mock に与えられる引数を確認することでログレベルを確認する
    # 以下の test_01〜05 では ログのエラーレベルを確認するために log_print に mock.patch を使う
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
        # print("args:", args)
        self.assertEqual(args[0], expect_log_level)

    # add に mock.patch を使った正常形のテスト
    # add の中身を実行せず、add の戻り値を任意に指定したテストができる
    # add の引数は与えているが評価しないので任意の値でよい
    def test_02_main_ok_mock(self):
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
        # print("args:", args)
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # main の戻り値を確認
        self.assertEqual(result, expect)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        # print("args:", args)
        self.assertEqual(args[0], expect_log_level)

    # add に mock.patch を使わない異常形のテスト
    # add関数で RuntimeError が起こるための a, b の条件を設定している
    def test_03_main_ng_warning(self):
        """main関数の異常形 - add で RuntimeError 例外が上がる場合

        条件: a, b いずれかが正の整数でない (例 a=0, b=2)、関数 add で例外 RuntimeError が上がる
        期待値: main で例外をキャッチして、ログレベル "WARNING"
        """
        a, b = 0, 2
        # 期待値
        expect_log_level = "WARNING"

        # ログ出力関数を mock で patch
        with patch("mytool.log_print") as mock_log_print:
            main(a, b)

        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        # print("args:", args)
        self.assertEqual(args[0], expect_log_level)

    # add に mock.patch を使った異常形のテスト
    # add の mock に side_effect を設定して例外 RuntimeError を発生させる
    def test_04_main_ng_warning_mock(self):
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
        # print("args:", args)
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        # print("args:", args)
        self.assertEqual(args[0], expect_log_level)
        self.assertIn(expect_log_msg, args[1])

    # add に mock.patch を使った異常形のテスト
    # add の mock に side_effect を設定して RuntimeError 以外の例外を発生させる
    # Exception をキャッチすればは通常使われる全ての例外できる
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
        # print("args:", args)
        self.assertEqual(args[0], a)
        self.assertEqual(args[1], b)
        # log_print の引数を確認
        args, _kwargs = mock_log_print.call_args
        # print("args[0]:", args[0])
        # print("args[1]:", args[1])
        self.assertEqual(args[0], expect_log_level)
        self.assertIn(expect_log_msg, args[1])
