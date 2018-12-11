echo "vangogh-content7"
python3 main.py --style=styles/vangogh.jpg --content=contents/content7.jpg 
echo "vangogh-content7-chol"
python3 main.py --style=styles/vangogh.jpg --content=contents/content7.jpg --color_preserve=True 
echo "vangogh-content7-pca"
python3 main.py --style=styles/vangogh.jpg --content=contents/content7.jpg --color_preserve=True --preserve_mode='pca'
echo "vangogh-content7-lum"
python3 main.py --style=styles/vangogh.jpg --content=contents/content7.jpg --color_preserve=True --preserve_mode='lum'
