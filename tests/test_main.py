import fire

from main import MainDefaultTest


class TestMain:

    def test_01_hi_should_salute(self, capsys):
        fire.Fire(MainDefaultTest, ['test'])
        out, err = capsys.readouterr()
        assert out == "Hi, test\n"
