from lxml import etree
import sys

def main():
    tree = etree.iterparse(sys.argv[1])
    print(type(tree))
    for event, elem in tree:
        print('%s\n' % elem.text.encode('utf-8'))



if __name__ == "__main__":
    main()

