import cimoc2moe

# 从Cimoc获得的漫画文件夹
d = 'F:\\file'

a = cimoc2moe.Cimoc2Mox(source=d)
a.read()
a.copy()
a.zipping()
