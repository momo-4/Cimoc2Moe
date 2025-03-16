import cimoc2moe

# 从Cimoc获得的漫画文件夹
dir = "F:\\file"

c2m = cimoc2moe.Cimoc2Mox(source=dir)
c2m.read()
c2m.copy()
c2m.zipping()
