from mytool import add, main
import unittest
from unittest.mock import patch


class TestAdd(unittest.TestCase):
    """add関数のテスト"""

    def test_01_add_ok(self):
        """add関数の正常形
        条件: a,b いずれも正の整数 (例 a=1, b=2)
        期待値: 戻り値がaとbの輪 (例 戻り値 3)
        """
        a, b = 1, 2
        expect = 3

        result = add(a, b)

        self.assertEqual(result, expect)

    def test_02_add_ng(self):
        """add関数の異常形
        条件: a, b いずれかが正の整数でない (例 a=0, b=2)
        期待値: 例外 RuntimeError が上がる、
            例外メッセージ: "Given argunents a and b must be positive integers."
        """
        a, b = 0, 2
        expect = RuntimeError
        expect_msg = "Given argunents a and b must be positive integers."

        with self.assertRaises(expect) as e:
            add(a, b)

        # 例外情報の値に含まれる文字列を確認
        # print(e.exception.args[0])
        self.assertIn(expect_msg, e.exception.args[0])


class TestMain(unittest.TestCase):
    """main関数のテスト"""

    def test_01_main_ok(self):
        """main関数の正常形
        条件: a,b いずれも正の整数 (例 a=1, b=2)
        期待値: 戻り値がaとbの輪 (例 戻り値 3), ログレベル "INFO"
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

    def test_02_main_ok_mock(self):
        """main関数の正常形 - addをmockでpatch
        条件: a,b いずれも正の整数 (例 a=1, b=2)
        期待値: 戻り値がaとbの輪 (例 戻り値 3), ログレベル "INFO"
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

    def test_03_main_ng_warning(self):
        """main関数の異常形 - ログレベル "WARNING"
        条件: a, b いずれかが正の整数でない (例 a=0, b=2)
        期待値: 関数 add で例外 RuntimeError が上がり、main でキャッチする。
            ログレベル "WARNING"
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

    def test_04_main_ng_warning_mock(self):
        """main関数の異常形 - ログレベル "WARNING" add関数をmockでpatch
        条件: a, b いずれも正の整数 (例 a=1, b=2) (mockなので任意)
        期待値: 関数 add で例外 RuntimeError が上がり、main でキャッチする。
            ログレベル "WARNING"
        """
        a, b = 1, 2
        mock_side_eff = RuntimeError("テスト例外")
        # 期待値
        expect_log_level = "WARNING"

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

    def test_05_main_ng_error_mock(self):
        """main関数の異常形 - ログレベル "ERROR" add関数をmockでpatch
        条件: a, b いずれも正の整数 (例 a=1, b=2) (mockなので任意)
        期待値: 関数 add で例外 RuntimeError 以外の例外が上がり、main でキャッチする。
            ログレベル "ERROR"
        """
        a, b = 1, 2
        mock_side_eff = Exception("テスト例外")
        # 期待値
        expect_log_level = "ERROR"

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
