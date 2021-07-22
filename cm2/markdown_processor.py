class MarkdownProcessor:
    def replace_invalid_quotes(self, given_markdown_str):
        given_markdown_str = given_markdown_str.replace('“', '"')
        given_markdown_str = given_markdown_str.replace('”', '"')
        return given_markdown_str