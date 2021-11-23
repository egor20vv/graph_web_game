
def main():
    html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test</title>
</head>
<body>

Просто {текст} {} ААААА <br>

Тут переменная name: %{name} ААААА <br>

</body>
</html>
    """
    some_name = 'Egor'
    test_str = '{name}'.format(name=some_name)
    print('')


if __name__ == '__main__':
    main()

    # TODO https://fastapi.tiangolo.com/advanced/templates/

