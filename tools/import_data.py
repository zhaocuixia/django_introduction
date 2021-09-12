import os
import django
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_introduction.settings")
django.setup()
from blog.models import Article

def main():
    content_list = []
    os.getcwd()
    os.chdir("..")
    a = os.getcwd()
    sys.path.append(a)
    data_path = 'data/article'
    files = os.listdir(data_path)
    print(files)
    for name in files:
        f = os.path.join(data_path, name)
        with open(f, 'r', encoding='utf-8') as f:
            content = f.read()
            item = (name[:-4], content[:100], content)  # title 不要TXT，摘要，内容
            content_list.append(item)

    for item in content_list:
        print("saving article :%s" % item[0])
        article = Article()
        article.title = item[0]
        article.brief_content = item[1]
        article.content = item[2]
        article.save()

if __name__ == '__main__':
    main()