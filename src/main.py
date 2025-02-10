from textnode import TextNode
from textnode import TextType

def main():
    test = TextNode("text node", TextType.ITALIC, "url.com")
    print(repr(test))
    

if __name__ == "__main__":
    main()    
    