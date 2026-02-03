from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json 


from .models import DichVu, LichHen, ChiNhanh
from .forms import DangKyForm, DangNhapForm


# PHẦN 1: CÁC TRANG CHÍNH (FRONTEND)


def index(request):
    """Trang chủ: Hiển thị Popup đặt lịch với danh sách Dịch vụ & Chi nhánh"""
    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all()
    return render(request, 'nhakhoa/index.html', {'ds_dv': ds_dv, 'ds_cn': ds_cn})

def gioithieu(request):

    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all()
    return render(request, 'nhakhoa/gioithieu.html', {'ds_dv': ds_dv, 'ds_cn': ds_cn})

def dichvu(request):
    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all() 
    return render(request, 'nhakhoa/dichvu.html', {'ds_dv': ds_dv, 'ds_cn': ds_cn})

def lienhe(request):
    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all()
    return render(request, 'nhakhoa/lienhe.html', {'ds_dv': ds_dv, 'ds_cn': ds_cn})


# PHẦN 2: CHỨC NĂNG GIS & BẢN ĐỒ (QUAN TRỌNG)


def chinhanh(request):
    ds_cn = ChiNhanh.objects.all()
    ds_dv = DichVu.objects.all()
    return render(request, 'nhakhoa/chinhanh.html', {'ds_cn': ds_cn, 'ds_dv': ds_dv})

def ban_do_so(request):
    """
    Trang bản đồ số GIS "Full Option":
    1. Hiển thị Marker các chi nhánh.
    2. Cung cấp dữ liệu cho Form đặt lịch.
    3. Hiển thị danh sách Lịch sử khách hàng (CÓ PHÂN QUYỀN).
    """
    
    # --- 1. DỮ LIỆU CHO FORM ĐẶT LỊCH ---
    ds_dv = DichVu.objects.all()
    ds_cn = ChiNhanh.objects.all()

    # --- 2. DỮ LIỆU CHO BẢN ĐỒ (MARKER CHI NHÁNH) ---
    data_chi_nhanh = []
    for cn in ds_cn:
        try:
            
            lat = float(str(cn.vi_do).replace(',', '.'))
            lng = float(str(cn.kinh_do).replace(',', '.'))
            
            data_chi_nhanh.append({
                'id': cn.id,
                'ten': cn.ten_chi_nhanh,
                'dia_chi': cn.dia_chi,
                'lat': lat,
                'lng': lng,
            })
        except ValueError: continue
    
    # --- 3. DỮ LIỆU CHO SIDEBAR (LỊCH SỬ KHÁCH HÀNG - CÓ PHÂN QUYỀN) ---
    
  
    if request.user.is_authenticated:
        if request.user.is_staff:
       
            ds_lich_hen = LichHen.objects.select_related('chi_nhanh', 'dich_vu').all().order_by('-id')
        else:
     
            ds_lich_hen = LichHen.objects.select_related('chi_nhanh', 'dich_vu').filter(email=request.user.email).order_by('-id')
    else:
  
        ds_lich_hen = []
    

    data_lich_su = []
    for lh in ds_lich_hen:
        if lh.chi_nhanh: 
            try:
                lat = float(str(lh.chi_nhanh.vi_do).replace(',', '.'))
                lng = float(str(lh.chi_nhanh.kinh_do).replace(',', '.'))
                
                data_lich_su.append({
                    'id': lh.id,
                    'ten_khach': lh.ho_ten,
                    'sdt': lh.so_dien_thoai,
                    'dich_vu': lh.dich_vu.ten_dich_vu if lh.dich_vu else "Dịch vụ khác",
                    'ngay_hen': lh.ngay_hen_mong_muon.strftime("%d/%m/%Y") if lh.ngay_hen_mong_muon else "Chưa rõ",
                    'ten_chi_nhanh': lh.chi_nhanh.ten_chi_nhanh,
                    'lat': lat,
                    'lng': lng
                })
            except: continue

  
    context = {
        'json_chi_nhanh': json.dumps(data_chi_nhanh),
        'json_lich_su': json.dumps(data_lich_su),
        'ds_dv': ds_dv,
        'ds_cn': ds_cn
    }

    return render(request, 'nhakhoa/bandoso.html', context)


# PHẦN 3: CHỨC NĂNG TÀI KHOẢN (AUTH)


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


# PHẦN 4: LOGIC ĐẶT LỊCH & XÁC NHẬN


def dat_lich(request):
    """Xử lý form đặt lịch từ trang chủ"""
    if request.method == 'POST':
        ho_ten = request.POST.get('ho_ten')
        sdt = request.POST.get('sdt')
        email = request.POST.get('email')
        

        chi_nhanh_id = request.POST.get('chi_nhanh')
        dich_vu_id = request.POST.get('dich_vu')
        
        ngay_hen = request.POST.get('ngay_hen')
        noi_dung = request.POST.get('noi_dung')


        try:
            chi_nhanh_obj = ChiNhanh.objects.get(id=chi_nhanh_id)
        except:
            chi_nhanh_obj = None

        try:
            dich_vu_obj = DichVu.objects.get(id=dich_vu_id)
        except:
            dich_vu_obj = None
            
        if not ngay_hen: ngay_hen = None

        new_app = LichHen.objects.create(
            ho_ten=ho_ten,
            so_dien_thoai=sdt,
            email=email,
            chi_nhanh=chi_nhanh_obj,
            dich_vu=dich_vu_obj,
            ngay_hen_mong_muon=ngay_hen,
            noi_dung=noi_dung
        )
        
        return redirect('xac_nhan_lich_hen', id_lich_hen=new_app.id)
        
    return redirect('index')

def xac_nhan_lich_hen(request, id_lich_hen):
    """Trang hiển thị phiếu xác nhận + Bản đồ Leaflet"""
    try:
        lich_hen = LichHen.objects.get(id=id_lich_hen)
        
        # Logic GIS: Lấy tọa độ để truyền sang JavaScript
        if lich_hen.chi_nhanh:
            toa_do_lat = lich_hen.chi_nhanh.vi_do
            toa_do_lng = lich_hen.chi_nhanh.kinh_do
            dia_chi_text = lich_hen.chi_nhanh.dia_chi
        else:
            toa_do_lat = "0"
            toa_do_lng = "0"
            dia_chi_text = "Chưa có thông tin địa chỉ"

        context = {
            'lich_hen': lich_hen,
            'lat': toa_do_lat,   
            'lng': toa_do_lng,   
            'address': dia_chi_text
        }
        
        return render(request, 'nhakhoa/datlich.html', context)
        
    except LichHen.DoesNotExist:
        return redirect('index')

def lich_su(request):
    """Trang xem lịch sử khám bệnh cũ (Dạng bảng)"""
    if not request.user.is_authenticated:
        messages.warning(request, "Vui lòng đăng nhập để xem lịch sử!")
        return redirect('dangnhap')
    
    if request.user.is_staff:
        ds_lich = LichHen.objects.all().order_by('-id')
    else:
        ds_lich = LichHen.objects.filter(email=request.user.email).order_by('-id')

    return render(request, 'nhakhoa/lichsu.html', {'ds_lich': ds_lich})