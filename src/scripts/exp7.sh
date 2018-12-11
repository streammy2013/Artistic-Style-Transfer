echo "picabia-content9"
python3 main.py --style=styles/picabia.jpg --content=contents/content9.jpg 
echo "picabia-content9-chol"
python3 main.py --style=styles/picabia.jpg --content=contents/content9.jpg --color_preserve=True 
echo "picabia-content9-pca"
python3 main.py --style=styles/picabia.jpg --content=contents/content9.jpg --color_preserve=True --preserve_mode='pca'
echo "picabia-content9-lum"
python3 main.py --style=styles/picabia.jpg --content=contents/content9.jpg --color_preserve=True --preserve_mode='lum'
