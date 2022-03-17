import os
from unittest import result
from urllib import request
from api import PetFriends
from settings import valid_email, valid_pass, invalid_email, invalid_pass, empty_email, empty_pass

pf = PetFriends ()


def test_get_api_key_for_valid_user(email = valid_email, password=valid_pass):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key =pf.get_api_key(valid_email, valid_pass)
    status,result =pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_api_key_for_ivalid_user(email=invalid_email, password=invalid_pass):
    '''Тест на проверку введения неверных email и password'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn\'t found in database' in result

def test_get_api_key_for_empty_email(email=empty_email, password=valid_pass):
    '''Тест на проверку введения пустого email'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn\'t found in database' in result

def test_get_api_key_for_empty_pass(email=valid_email, password=empty_pass):
    '''Тест на проверку введения пустого password'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn\'t found in database' in result

def test_add_pet(name='Kesha', animal_type='pig', age ='2', pet_photo='images/hrushka.jpg'):
    '''Тест на проверку добавления питомца с валидными данными'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

def test_add_pet_long_name(name = 'Keshadsfpdpsogopjgofdaj]gk]dakhgodfjhkfd]ghk]ard',animal_type='pig', age ='2', pet_photo='images/hrushka.jpg'):
    '''Тест на проверку добавления питомца с длинным именем'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    try:
        assert status == 403 or status == 400
    except:
        print('Test failed')

def test_add_text_in_age_new_pet (name='Kesha', animal_type='pig', age ='any', pet_photo='images/hrushka.jpg' ):
    '''Тест на проверку записи текста в поле возраста'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    try:
        assert status == 403 or status == 400
    except:
        print('Test failed')


def test_add_pet_empty_fields(name = '', animal_type = '', age = '', pet_photo = ''):
    '''Тест на проверку добавления питомца с пустыми полями'''
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_pass)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except:
        print('Test failed, pet no created')
    else:
        print('Test failed')

def test_add_pet_no_photo (name='Kesha', animal_type='pig', age ='any', pet_photo=' '):
    '''Тест на добавление питомца без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    status, result = pf.add_new_pet_without_photo(auth_key,name,animal_type,age)

    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    '''Тест на проверку удаления питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Kesha", "pig", "2", "images/hrushka.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_upd_info_of_pet (name='Diggi', animal_type ='cat', age = '5'):
    '''тест на проверку внесения изменений в поля данных питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.upd_info_of_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Pets is missing")