"""Bundle lecture 04 as one HTML, including lecture 03's unchanged factor module."""
from pathlib import Path
from urllib.parse import quote
import re


def build() -> Path:
    root=Path(__file__).resolve().parents[1]
    course=root/'extras/lecture-04'
    page=course/'index.html'
    html=page.read_text(encoding='utf-8')
    for tag,name in [('style','course.css'),('script','course.js')]:
        source=(course/name).read_text(encoding='utf-8')
        if f'</{tag}' in source.lower():
            raise ValueError(f'Closing HTML tag in {name}')
        block=f'<!-- course-{tag}:start -->\n<{tag} id="course-{tag}">\n{source.rstrip()}\n</{tag}>\n<!-- course-{tag}:end -->'
        marker=f'<!-- course-{tag}:start -->'
        if marker in html:
            html,n=re.subn(rf'{marker}.*?<!-- course-{tag}:end -->',lambda _:block,html,flags=re.S)
            if n!=1:raise ValueError(f'Expected one {tag} block')
        elif tag=='style':
            html,n=re.subn('<link rel="stylesheet" href="course.css">',lambda _:block,html)
            if n!=1:raise ValueError('Expected one stylesheet')
        else:
            html=html.replace('<script src="course.js" defer></script>','')
            if html.count('</body>')!=1:raise ValueError('Expected one body end')
            html=html.replace('</body>',block+'\n</body>')
    for name in ['evaluation_lab.py','factor_lab.py','requirements.txt','plot_evaluation.py','requirements-plot.txt']:
        path=course/name if name!='factor_lab.py' else root/'extras/lecture-03/factor_lab.py'
        mime='text/x-python' if name.endswith('.py') else 'text/plain'
        data=f'data:{mime};charset=utf-8,'+quote(path.read_text(encoding='utf-8'),safe='')
        pattern=rf'<a\b[^>]*(?:href="{re.escape(name)}"|data-course-file="{re.escape(name)}")[^>]*>'
        def embed(match):
            tag=re.sub(r'\s(?:href|download|data-course-file)="[^"]*"|\sdownload(?=\s|>)','',match.group(0))
            return tag[:-1]+f' data-course-file="{name}" href="{data}" download="{name}">'
        html,n=re.subn(pattern,embed,html)
        if n==0:raise ValueError(f'Missing download link: {name}')
    base='https://github.com/ThreshoLdnnis/Quant-for-babies/blob/main/'
    for local,remote in {'../../README.md':'README.md','README.md':'extras/lecture-04/README.md','../lecture-03/index.html':'extras/lecture-03/index.html'}.items():
        html=html.replace(f'href="{local}"',f'href="{base}{remote}"')
    page.write_text(html,encoding='utf-8')
    return page


if __name__=='__main__':print(build())
