import os
import sounddevice as sd
from scipy.io.wavfile import write

record_category = {
    'Thời sự': 'thoi_su',
    'Góc nhìn': 'goc_nhin',
    'Thế giới': 'the_gioi',
    'Kinh doanh': 'kinh_doanh',
    'Giải trí': 'giai_tri',
    'Thể thao': 'the_thao', 
    'Pháp luật': 'phap_luat', 
    'Giáo dục': 'giao_duc', 
    'Sức khỏe': 'suc_khoe',
    'Đời sống': 'doi_song', 
    'Du lịch': 'du_lich',
    'Khoa học': 'khoa_hoc',
    'Số hóa': 'so_hoa',
    'Xe': 'xe',
    'Ý kiến': 'y_kien',
    'Tâm sự': 'tam_su'
}

def record(category, article_url, article_sentence, sentence_number, total):
    if(int(sentence_number) > int(total)):
        return
    file_data_name = record_category[category] + '.txt'
    file_data_path = 'record/record_data/' + record_category[category] + '/' + file_data_name
    file_voice_name = record_category[category] + '_' + str(sentence_number) + '.wav'
    voice_data_path = 'record/record_data/' + record_category[category] + '/' +file_voice_name 

    if os.path.exists(file_data_path):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    data_file = open(file_data_path, append_write)
    
    if(int(sentence_number) == 1): 
        print('hello')
        data_file.write(article_url + '\n' + file_voice_name + '\n' + article_sentence + '\n')
    elif (int(sentence_number) > 1 and int(sentence_number) < int(total)):
        data_file.write(file_voice_name + '\n' + article_sentence + '\n')
    elif (int(sentence_number) == int(total)):
        data_file.write(file_voice_name + '\n' + article_sentence + '\n')
        print('Recording article ' + article_url + ' successfully!')

    sd.default.device = 0
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print('Recording...')
    sd.wait()  # Wait until recording is finished
    write(voice_data_path, fs, myrecording)  # Save

    return 'Recording sentence ' + str(sentence_number) + ' successfully!'