from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Import đầy đủ các Model
from .models import DichVu, LichHen, ChiNhanh
from .forms import DangKyForm, DangNhapForm

# ==========================================
# PHẦN 1: CÁC TRANG CHÍNH CỦA WEBSITE
# ==========================================

def index(request):
    # Lấy danh sách Dịch vụ & Chi nhánh để hiển thị lên Popup đặt lịch
    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all()
    return render(request, 'nhakhoa/index.html', {'ds_dv': ds_dv, 'ds_cn': ds_cn})

def gioithieu(request):
    return render(request, 'nhakhoa/gioithieu.html')

def dichvu(request):
    dulieu_dichvu = DichVu.objects.all()
    return render(request, 'nhakhoa/dichvu.html', {'ds_dv': dulieu_dichvu})

# --- HÀM QUAN TRỌNG: TRANG BẢN ĐỒ GIS ---
def chinhanh(request):
    # Lấy danh sách chi nhánh từ Database để vẽ lên bản đồ Leaflet
    ds_cn = ChiNhanh.objects.all()
    return render(request, 'nhakhoa/chinhanh.html', {'ds_cn': ds_cn})

def lienhe(request):
    return render(request, 'nhakhoa/lienhe.html')


# ==========================================
# PHẦN 2: CHỨC NĂNG TÀI KHOẢN (AUTH)
# ==========================================

def dangky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công! Hãy đăng nhập.')
            return redirect('dangnhap')
    else:
        form = DangKyForm()
    return render(request, 'nhakhoa/dangky.html', {'form': form})

def dangnhap(request):
    if request.method == 'POST':
        form = DangNhapForm(request.POST)
        if form.is_valid():
            username_input = form.cleaned_data['username']
            password_input = form.cleaned_data['password']
            user = authenticate(request, username=username_input, password=password_input)
            
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/admin/') 
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu!')
    else:
        form = DangNhapForm()
    return render(request, 'nhakhoa/dangnhap.html', {'form': form})

def dangxuat(request):
    logout(request)
    return redirect('index')


# ==========================================
# PHẦN 3: LOGIC GIS & ĐẶT LỊCH (NÂNG CAO)
# ==========================================

def dat_lich(request):
    if request.method == 'POST':
        ho_ten = request.POST.get('ho_ten')
        sdt = request.POST.get('sdt')
        email = request.POST.get('email')
        
        # Lấy ID từ form (do người dùng chọn trong thẻ Select)
        chi_nhanh_id = request.POST.get('chi_nhanh')
        dich_vu_id = request.POST.get('dich_vu')
        
        ngay_hen = request.POST.get('ngay_hen')
        noi_dung = request.POST.get('noi_dung')

        # 1. Truy vấn Object Chi Nhánh (GIS) từ Database
        # Để lấy được tọa độ sau này, ta phải lưu ID chi nhánh vào cột ForeignKey
        try:
            chi_nhanh_obj = ChiNhanh.objects.get(id=chi_nhanh_id)
        except:
            chi_nhanh_obj = None

        # 2. Truy vấn Object Dịch Vụ
        try:
            dich_vu_obj = DichVu.objects.get(id=dich_vu_id)
        except:
            dich_vu_obj = None
            
        if not ngay_hen: ngay_hen = None

        # 3. Lưu vào Database (Bảng LichHen)
        new_app = LichHen.objects.create(
            ho_ten=ho_ten,
            so_dien_thoai=sdt,
            email=email,
            chi_nhanh=chi_nhanh_obj, # Lưu object ChiNhanh (có chứa tọa độ bên trong)
            dich_vu=dich_vu_obj,
            ngay_hen_mong_muon=ngay_hen,
            noi_dung=noi_dung
        )
        
        # Chuyển hướng sang trang xác nhận thành công (kèm ID vừa tạo)
        return redirect('xac_nhan_lich_hen', id_lich_hen=new_app.id)
        
    return redirect('index')

def xac_nhan_lich_hen(request, id_lich_hen):
    try:
        # Lấy thông tin phiếu hẹn vừa tạo
        lich_hen = LichHen.objects.get(id=id_lich_hen)
        
        # Logic GIS: Lấy tọa độ từ Database của chi nhánh mà khách đã chọn
        # Dữ liệu này sẽ được dùng cho thuật toán Haversine và Google Maps Routing
        if lich_hen.chi_nhanh:
            toa_do_lat = lich_hen.chi_nhanh.vi_do
            toa_do_lng = lich_hen.chi_nhanh.kinh_do
            map_url = lich_hen.chi_nhanh.link_google_map
            dia_chi_text = lich_hen.chi_nhanh.dia_chi
        else:
            toa_do_lat = "Chưa xác định"
            toa_do_lng = "Chưa xác định"
            map_url = ""
            dia_chi_text = "Chưa có thông tin địa chỉ"

        context = {
            'lich_hen': lich_hen,
            'lat': toa_do_lat,   # Truyền Vĩ độ sang HTML
            'lng': toa_do_lng,   # Truyền Kinh độ sang HTML
            'map_url': map_url,
            'address': dia_chi_text
        }
        
        # Render trang 'datlich.html' (nơi chứa Script tính khoảng cách)
        return render(request, 'nhakhoa/datlich.html', context)
        
    except LichHen.DoesNotExist:
        return redirect('index')
    # --- Thêm vào cuối file nhakhoa/views.py ---

def lich_su(request):

    if not request.user.is_authenticated:
        messages.warning(request, "Vui lòng đăng nhập để xem lịch sử!")
        return redirect('dangnhap')
    
    if request.user.is_staff:
        ds_lich = LichHen.objects.all().order_by('-id')
    else:
        ds_lich = LichHen.objects.filter(email=request.user.email).order_by('-id')

    return render(request, 'nhakhoa/lichsu.html', {'ds_lich': ds_lich})