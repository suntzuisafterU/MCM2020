import matplotlib.pyplot as plt
img = plt.imread("images/Soccer_Field_Transparant.png")
fig, ax = plt.subplots()
ax.imshow(img)
plt.show()