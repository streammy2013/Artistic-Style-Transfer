echo "picasso-content9"
python3 main.py --style=styles/picasso.jpg --content=contents/content9.jpg 
echo "picasso-content9-chol"
python3 main.py --style=styles/picasso.jpg --content=contents/content9.jpg --color_preserve=True 
echo "picasso-content9-pca"
python3 main.py --style=styles/picasso.jpg --content=contents/content9.jpg --color_preserve=True --preserve_mode='pca'
echo "picasso-content9-lum"
python3 main.py --style=styles/picasso.jpg --content=contents/content9.jpg --color_preserve=True --preserve_mode='lum'
