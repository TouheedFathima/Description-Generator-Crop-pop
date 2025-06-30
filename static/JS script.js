function toggleCustomTimeCommitment(selectId, customInputId1, customInputId2) {
  const select = document.getElementById(selectId);
  const customInput1 = document.getElementById(customInputId1);
  const customInput2 = document.getElementById(customInputId2);
  const display = select.value === 'Customize' ? 'block' : 'none';
  customInput1.style.display = display;
  customInput2.style.display = display;
  if (select.value !== 'Customize') {
    customInput1.value = '';
    customInput2.value = '';
  }
}

function toggleCustomIdentity(selectId, customInputId) {
  const select = document.getElementById(selectId);
  const customInput = document.getElementById(customInputId);
  
  if (!select) {
    console.error(`Select element with ID '${selectId}' not found.`);
    return;
  }
  if (!customInput) {
    console.error(`Custom input element with ID '${customInputId}' not found.`);
    return;
  }

  console.log(`Toggling custom identity for select '${selectId}', value: '${select.value}'`);
  
  const display = select.value === 'Other' ? 'block' : 'none';
  customInput.style.display = display;
  
  if (select.value !== 'Other') {
    customInput.value = '';
    const errorElement = document.getElementById(`${selectId}-error`);
    if (errorElement) {
      errorElement.textContent = '';
    } else {
      console.warn(`Error element with ID '${selectId}-error' not found.`);
    }
  }
}

function showCreateForm() {
  document.getElementById('createForm').style.display = 'block';
  document.getElementById('passForm').style.display = 'none';
  showCreateCompanyForm();
}

function showPassForm() {
  document.getElementById('createForm').style.display = 'none';
  document.getElementById('passForm').style.display = 'block';
  showPassCompanyForm();
}

function showCreateCompanyForm() {
  document.getElementById('createCompanyForm').style.display = 'block';
  document.getElementById('createIndividualForm').style.display = 'none';
  document.getElementById('createCompanyDescription').style.display = 'block';
  document.getElementById('createIndividualDescription').style.display = 'none';
  document.getElementById('passCompanyDescription').style.display = 'none';
  document.getElementById('passIndividualDescription').style.display = 'none';
}

function showCreateIndividualForm() {
  document.getElementById('createCompanyForm').style.display = 'none';
  document.getElementById('createIndividualForm').style.display = 'block';
  document.getElementById('createCompanyDescription').style.display = 'none';
  document.getElementById('createIndividualDescription').style.display = 'block';
  document.getElementById('passCompanyDescription').style.display = 'none';
  document.getElementById('passIndividualDescription').style.display = 'none';
}

function showPassCompanyForm() {
  document.getElementById('passCompanyForm').style.display = 'block';
  document.getElementById('passIndividualForm').style.display = 'none';
  document.getElementById('createCompanyDescription').style.display = 'none';
  document.getElementById('createIndividualDescription').style.display = 'none';
  document.getElementById('passCompanyDescription').style.display = 'block';
  document.getElementById('passIndividualDescription').style.display = 'none';
}

function showPassIndividualForm() {
  document.getElementById('passCompanyForm').style.display = 'none';
  document.getElementById('passIndividualForm').style.display = 'block';
  document.getElementById('createCompanyDescription').style.display = 'none';
  document.getElementById('createIndividualDescription').style.display = 'none';
  document.getElementById('passCompanyDescription').style.display = 'none';
  document.getElementById('passIndividualDescription').style.display = 'block';
}

function toggleExperienceFields() {
  const fresherCheckbox = document.getElementById('fresherCheckbox');
  const experienceMin = document.getElementById('experienceMin');
  const experienceMax = document.getElementById('experienceMax');
  
  if (fresherCheckbox.checked) {
    experienceMin.disabled = true;
    experienceMax.disabled = true;
    experienceMin.value = '';
    experienceMax.value = '';
    document.getElementById('preferredExperience').value = 'Fresher';
  } else {
    experienceMin.disabled = false;
    experienceMax.disabled = false;
    updateExperienceValue();
  }
}

function updateExperienceValue() {
  const fresherCheckbox = document.getElementById('fresherCheckbox');
  if (fresherCheckbox.checked) {
    document.getElementById('preferredExperience').value = 'Fresher';
    return;
  }

  const min = document.getElementById('experienceMin').value;
  const max = document.getElementById('experienceMax').value;
  let experienceValue = '';

  if (min && max) {
    experienceValue = `${min}-${max} years`;
  } else if (min) {
    experienceValue = `${min} years minimum`;
  } else if (max) {
    experienceValue = `Up to ${max} years`;
  } else {
    experienceValue = '';
  }

  document.getElementById('preferredExperience').value = experienceValue;
}

function toggleIndividualExperienceFields() {
  const fresherCheckbox = document.getElementById('individualFresherCheckbox');
  const experienceMin = document.getElementById('individualExperienceMin');
  const experienceMax = document.getElementById('individualExperienceMax');
  
  if (fresherCheckbox.checked) {
    experienceMin.disabled = true;
    experienceMax.disabled = true;
    experienceMin.value = '';
    experienceMax.value = '';
    document.getElementById('individualPreferredExperience').value = 'Fresher';
  } else {
    experienceMin.disabled = false;
    experienceMax.disabled = false;
    updateIndividualExperienceValue();
  }
}

function updateIndividualExperienceValue() {
  const fresherCheckbox = document.getElementById('individualFresherCheckbox');
  if (fresherCheckbox.checked) {
    document.getElementById('individualPreferredExperience').value = 'Fresher';
    return;
  }

  const min = document.getElementById('individualExperienceMin').value;
  const max = document.getElementById('individualExperienceMax').value;
  let experienceValue = '';

  if (min && max) {
    experienceValue = `${min}-${max} years`;
  } else if (min) {
    experienceValue = `${min} years minimum`;
  } else if (max) {
    experienceValue = `Up to ${max} years`;
  } else {
    experienceValue = '';
  }

  document.getElementById('individualPreferredExperience').value = experienceValue;
}

function togglePassExperienceFields() {
  const fresherCheckbox = document.getElementById('passFresherCheckbox');
  const experienceMin = document.getElementById('passExperienceMin');
  const experienceMax = document.getElementById('passExperienceMax');
  
  if (fresherCheckbox.checked) {
    experienceMin.disabled = true;
    experienceMax.disabled = true;
    experienceMin.value = '';
    experienceMax.value = '';
    document.getElementById('passPreferredExperience').value = 'Fresher';
  } else {
    experienceMin.disabled = false;
    experienceMax.disabled = false;
    updatePassExperienceValue();
  }
}

function updatePassExperienceValue() {
  const fresherCheckbox = document.getElementById('passFresherCheckbox');
  if (fresherCheckbox.checked) {
    document.getElementById('passPreferredExperience').value = 'Fresher';
    return;
  }

  const min = document.getElementById('passExperienceMin').value;
  const max = document.getElementById('passExperienceMax').value;
  let experienceValue = '';

  if (min && max) {
    experienceValue = `${min}-${max} years`;
  } else if (min) {
    experienceValue = `${min} years minimum`;
  } else if (max) {
    experienceValue = `Up to ${max} years`;
  } else {
    experienceValue = '';
  }

  document.getElementById('passPreferredExperience').value = experienceValue;
}

function toggleEducationRequirements() {
  const notNecessaryCheckbox = document.getElementById('educationNotNecessary');
  const educationCheckboxes = document.getElementsByClassName('education-checkbox');
  
  if (notNecessaryCheckbox.checked) {
    for (let checkbox of educationCheckboxes) {
      checkbox.disabled = true;
      checkbox.checked = false;
    }
    document.getElementById('educationRequirements').value = 'Not Necessary';
  } else {
    for (let checkbox of educationCheckboxes) {
      checkbox.disabled = false;
    }
    updateEducationRequirements();
  }
}

function updateEducationRequirements() {
  const notNecessaryCheckbox = document.getElementById('educationNotNecessary');
  if (notNecessaryCheckbox.checked) {
    document.getElementById('educationRequirements').value = 'Not Necessary';
    return;
  }

  const educationCheckboxes = document.getElementsByClassName('education-checkbox');
  let selectedEducation = [];

  for (let checkbox of educationCheckboxes) {
    if (checkbox.checked) {
      selectedEducation.push(checkbox.value);
    }
  }

  document.getElementById('educationRequirements').value = selectedEducation.join(', ');
}

function togglePassEducationRequirements() {
  const notNecessaryCheckbox = document.getElementById('passEducationNotNecessary');
  const educationCheckboxes = document.getElementsByClassName('pass-education-checkbox');
  
  if (notNecessaryCheckbox.checked) {
    for (let checkbox of educationCheckboxes) {
      checkbox.disabled = true;
      checkbox.checked = false;
    }
    document.getElementById('passEducationRequirements').value = 'Not Necessary';
  } else {
    for (let checkbox of educationCheckboxes) {
      checkbox.disabled = false;
    }
    updatePassEducationRequirements();
  }
}

function updatePassEducationRequirements() {
  const notNecessaryCheckbox = document.getElementById('passEducationNotNecessary');
  if (notNecessaryCheckbox.checked) {
    document.getElementById('passEducationRequirements').value = 'Not Necessary';
    return;
  }

  const educationCheckboxes = document.getElementsByClassName('pass-education-checkbox');
  let selectedEducation = [];

  for (let checkbox of educationCheckboxes) {
    if (checkbox.checked) {
      selectedEducation.push(checkbox.value);
    }
  }

  document.getElementById('passEducationRequirements').value = selectedEducation.join(', ');
}

function showIndividualSalaryRange() {
  const salaryRangeDiv = document.getElementById('individualSalaryRange');
  salaryRangeDiv.style.display = salaryRangeDiv.style.display === 'none' ? 'block' : 'none';
}

function updateIndividualPackageValue() {
  const salaryFrom = document.getElementById('individualSalaryFrom').value;
  const salaryTo = document.getElementById('individualSalaryTo').value;
  let packageValue = '';

  if (salaryFrom && salaryTo) {
    packageValue = `₹${salaryFrom} - ₹${salaryTo}`;
  } else if (salaryFrom) {
    packageValue = `₹${salaryFrom} onwards`;
  } else if (salaryTo) {
    packageValue = `Up to ₹${salaryTo}`;
  }

  document.getElementById('individualPackage').value = packageValue;
}

async function generateDescription(type) {
  const descriptionResult = type === 'company' 
    ? document.getElementById('createCompanyDescription') 
    : document.getElementById('createIndividualDescription');
  
  descriptionResult.innerHTML = 'Generating description...';

  let data = { companyType: type };

  if (type === 'company') {
    data.companyName = document.getElementById('companyName').value || '';
    data.opportunityTitle = document.getElementById('opportunityTitle').value || '';
    data.opportunityType = document.getElementById('opportunityType').value || '';
    data.workDuration = document.getElementById('workDuration').value || '';
    data.location = document.getElementById('location').value || '';
    data.workMode = document.getElementById('workMode').value || '';
    data.numberOfOpenings = parseInt(document.getElementById('numberOfOpenings').value) || 1;
    data.lastDate = document.getElementById('lastDate').value || '';
    data.educationRequirements = document.getElementById('educationRequirements').value || '';
    data.industryExpertise = document.getElementById('industryExpertise').value || '';
    data.preferredExperience = document.getElementById('preferredExperience').value || '';
    data.skillsRequired = document.getElementById('skillsRequired').value || '';
    data.languagePreference = document.getElementById('languagePreference').value || '';
    data.genderPreference = document.getElementById('genderPreference').value || '';
    data.salaryMin = parseInt(document.getElementById('salaryMin').value) || 0;
    data.salaryMax = parseInt(document.getElementById('salaryMax').value) || 0;
    const timeCommitmentSelect = document.getElementById('timeCommitment').value;
    data.timeCommitment = timeCommitmentSelect === 'Customize' 
      ? document.getElementById('customTimeCommitment').value || ''
      : timeCommitmentSelect;

    const salaryOptionRadios = document.getElementsByName('salaryOption');
    data.salaryOption = '';
    for (const radio of salaryOptionRadios) {
      if (radio.checked) {
        data.salaryOption = radio.value;
        break;
      }
    }

    data.recruiterName = document.getElementById('recruiterName')?.value || '';
    data.phoneNumber = document.getElementById('phoneNumber')?.value || ''; 
    data.emailAddress = document.getElementById('emailAddress')?.value || '';

    console.log('Data being sent for company:', data);

    const requiredFields = [
      'location', 'workMode', 'numberOfOpenings', 'lastDate', 'skillsRequired', 'timeCommitment'
    ];
    for (const field of requiredFields) {
      if (!data[field]) {
        document.getElementById(`${field}-error`).textContent = 'This field is required';
        descriptionResult.innerHTML = 'Please fill in all required fields.';
        return;
      } else {
        document.getElementById(`${field}-error`).textContent = '';
      }
    }
  } else if (type === 'individual') {
    data.companyName = document.getElementById('individualCompanyName').value || 'Individual';
    data.postType = document.getElementById('individualPostType').value || '';
    const identitySelect = document.getElementById('individualIdentity').value;
    data.opportunityType = identitySelect === 'Other' 
      ? document.getElementById('customIndividualIdentity').value 
      : identitySelect;
    const fresherCheckbox = document.getElementById('individualFresherCheckbox').checked;
    data.eligibility = fresherCheckbox ? 'Freshers' : document.getElementById('individualPreferredExperience').value || 'Not specified';
    data.location = document.getElementById('individualLocation').value || 'Not specified';
    data.workMode = document.getElementById('individualWorkMode').value || '';
    data.workDuration = document.getElementById('individualWorkDuration').value || '';
    data.title = document.getElementById('individualTitle').value || '';
    data.package = document.getElementById('individualPackage')?.value || `${document.getElementById('individualSalaryFrom').value || 0} - ${document.getElementById('individualSalaryTo').value || 0}`;
    data.lastDate = document.getElementById('individualLastDate').value || '';
    data.vacancy = parseInt(document.getElementById('individualVacancy').value) || 1;
    data.skills = document.getElementById('individualSkills').value || '';
    data.keywords = document.getElementById('individualKeywords')?.value || '';
    data.industryExpertise = document.getElementById('individualIndustryExpertise').value || '';
    data.languagePreference = document.getElementById('individualLanguagePreference').value || '';
    data.genderPreference = document.getElementById('individualGenderPreference').value || '';
    const timeCommitmentSelect = document.getElementById('individualTimeCommitment').value;
    data.timeCommitment = timeCommitmentSelect === 'Customize' 
      ? document.getElementById('customIndividualTimeCommitment').value || ''
      : timeCommitmentSelect;

    const salaryOptionRadios = document.getElementsByName('individualSalaryOption');
    data.salaryOption = '';
    for (const radio of salaryOptionRadios) {
      if (radio.checked) {
        data.salaryOption = radio.value;
        break;
      }
    }

    console.log('Data being sent for individual:', data);

    const requiredFields = [
      'individualIdentity'
    ];
    for (const field of requiredFields) {
      const fieldValue = field === 'individualIdentity' ? data.opportunityType : document.getElementById(field).value;
      if (!fieldValue || (field === 'individualVacancy' && fieldValue < 1)) {
        document.getElementById(`${field}-error`).textContent = field === 'individualIdentity' && identitySelect === 'Other' ? 'Please specify your custom identity' : 'This field is required';
        descriptionResult.innerHTML = 'Please fill in all required fields.';
        return;
      } else {
        document.getElementById(`${field}-error`).textContent = '';
      }
    }
  }

  try {
    const response = await fetch('/generate-description', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Failed to generate description');
    }

    const result = await response.json();
    descriptionResult.innerHTML = result.description;
  } catch (error) {
    console.error('Error generating description:', error);
    descriptionResult.innerHTML = 'An error occurred while generating the description. Please try again.';
  }
}

async function generatePassWithAI() {
  const companyType = document.getElementById('passCompanyForm').style.display === 'block' ? 'company' : 'individual';
  const descriptionResult = companyType === 'company' 
    ? document.getElementById('passCompanyDescription') 
    : document.getElementById('passIndividualDescription');
  const extractedTextInputId = `extractedText_${companyType === 'company' ? 'passCompany' : 'passIndividual'}`;
  const extractedTextInput = document.getElementById(extractedTextInputId);

  console.log('Generating description for companyType:', companyType);
  console.log('Extracted Text Input ID:', extractedTextInputId);
  console.log('Extracted Text Value:', extractedTextInput ? extractedTextInput.value : 'Input not found');

  descriptionResult.innerHTML = 'Generating description...';

  const data = { 
    companyType,
    wordCount: 1000  
  };
  data.extractedText = extractedTextInput ? extractedTextInput.value.trim() : '';

  const hasUploadedImage = data.extractedText && data.extractedText.length > 0;
  console.log('Has Uploaded Image:', hasUploadedImage);

  if (companyType === 'company') {
    data.companyName = document.getElementById('passCompanyName').value || '';
    data.opportunityTitle = document.getElementById('passOpportunityTitle').value || '';
    data.opportunityType = document.getElementById('passOpportunityType').value || '';
    data.location = document.getElementById('passLocation').value || 'Not specified';
    data.workMode = document.getElementById('passWorkMode').value || 'Not specified';
    data.numberOfOpenings = parseInt(document.getElementById('passNumberOfOpenings').value) || 1;
    data.lastDate = document.getElementById('passLastDate').value || '';
    data.educationRequirements = document.getElementById('passEducationRequirements').value || 'Not specified';
    data.industryExpertise = document.getElementById('passIndustryExpertise').value || '';
    data.preferredExperience = document.getElementById('passPreferredExperience').value || 'Not specified';
    data.skillsRequired = document.getElementById('passSkillsRequired').value || '';
    data.languagePreference = document.getElementById('passLanguagePreference').value || '';
    data.genderPreference = document.getElementById('passGenderPreference').value || '';
    data.salaryMin = parseInt(document.getElementById('passSalaryMin').value) || 0;
    data.salaryMax = parseInt(document.getElementById('passSalaryMax').value) || 0;
    const timeCommitmentSelect = document.getElementById('passTimeCommitment').value;
    data.timeCommitment = timeCommitmentSelect === 'Customize' 
      ? document.getElementById('customPassTimeCommitment').value || ''
      : timeCommitmentSelect;
    data.recruiterName = document.getElementById('passRecruiterName').value || '';
    data.phoneNumber = document.getElementById('passPhoneNumber').value || '';
    data.emailAddress = document.getElementById('passEmailAddress').value || '';

    const salaryOptionRadios = document.getElementsByName('passSalaryOption');
    data.salaryOption = '';
    for (const radio of salaryOptionRadios) {
      if (radio.checked) {
        data.salaryOption = radio.value;
        break;
      }
    }

    if (data.salaryMin > data.salaryMax && data.salaryMax !== 0) {
      document.getElementById('passSalaryMin-error').textContent = 'Minimum salary cannot be greater than maximum salary';
      descriptionResult.innerHTML = 'Please correct the salary range.';
      return;
    } else {
      document.getElementById('passSalaryMin-error').textContent = '';
      document.getElementById('passSalaryMax-error').textContent = '';
    }
  } else {
    data.companyName = document.getElementById('passIndividualCompanyName').value || 'Individual';
    data.opportunityTitle = document.getElementById('passIndividualOpportunityTitle').value || '';
    const identitySelect = document.getElementById('passIndividualIdentity').value;
    data.opportunityType = identitySelect === 'Other' 
      ? document.getElementById('customPassIndividualIdentity').value 
      : identitySelect;
    data.location = document.getElementById('passIndividualLocation').value || 'Not specified';
    data.workMode = document.getElementById('passIndividualWorkMode').value || 'Not specified';
    data.numberOfOpenings = parseInt(document.getElementById('passIndividualNumberOfOpenings').value) || 1;
    data.lastDate = document.getElementById('passIndividualLastDate').value || '';
    data.educationRequirements = document.getElementById('passEducationRequirements').value || 'Not specified';
    data.industryExpertise = document.getElementById('passIndustryExpertise').value || '';
    data.preferredExperience = document.getElementById('passPreferredExperience').value || 'Not specified';
    data.skillsRequired = document.getElementById('passIndividualSkillsRequired').value || '';
    data.languagePreference = document.getElementById('passLanguagePreference').value || '';
    data.genderPreference = document.getElementById('passGenderPreference').value || '';
    data.salaryMin = parseInt(document.getElementById('passSalaryMin').value) || 0;
    data.salaryMax = parseInt(document.getElementById('passSalaryMax').value) || 0;
    const timeCommitmentSelect = document.getElementById('passIndividualTimeCommitment').value;
    data.timeCommitment = timeCommitmentSelect === 'Customize' 
      ? document.getElementById('customPassIndividualTimeCommitment').value || ''
      : timeCommitmentSelect;
    data.recruiterName = document.getElementById('passIndividualRecruiterName').value || '';
    data.phoneNumber = document.getElementById('passIndividualPhoneNumber').value || '';
    data.emailAddress = document.getElementById('passIndividualEmailAddress').value || '';

    const salaryOptionRadios = document.getElementsByName('passIndividualSalaryOption');
    data.salaryOption = '';
    for (const radio of salaryOptionRadios) {
      if (radio.checked) {
        data.salaryOption = radio.value;
        break;
      }
    }

    if (data.salaryMin > data.salaryMax && data.salaryMax !== 0) {
      document.getElementById('passSalaryMin-error').textContent = 'Minimum salary cannot be greater than maximum salary';
      descriptionResult.innerHTML = 'Please correct the salary range.';
      return;
    } else {
      document.getElementById('passSalaryMin-error').textContent = '';
      document.getElementById('passSalaryMax-error').textContent = '';
    }
  }

  try {
    const response = await fetch('/generate-pass-description', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      let errorMessage = 'Failed to generate description';
      try {
        const errorData = await response.json();
        console.error('Server error response:', errorData);
        errorMessage = errorData.error || response.statusText;
      } catch (e) {
        console.error('Failed to parse error response:', e);
      }
      throw new Error(`Failed to generate description: ${errorMessage}`);
    }

    const result = await response.json();
    descriptionResult.innerHTML = result.description;
  } catch (error) {
    console.error('Error generating description:', error);
    descriptionResult.innerHTML = `An error occurred: ${error.message}. Please try again.`;
  }
}

function formatText(command) {
  const descriptionBoxes = [
    'createCompanyDescription',
    'createIndividualDescription',
    'passCompanyDescription',
    'passIndividualDescription'
  ];
  let activeDescription = null;
  for (const boxId of descriptionBoxes) {
    const box = document.getElementById(boxId);
    if (box.style.display === 'block') {
      activeDescription = box;
      break;
    }
  }
  if (activeDescription) {
    activeDescription.focus();
    document.execCommand(command, false, null);
  }
}

function changeFont(font) {
  if (font) {
    const descriptionBoxes = [
      'createCompanyDescription',
      'createIndividualDescription',
      'passCompanyDescription',
      'passIndividualDescription'
    ];
    let activeDescription = null;
    for (const boxId of descriptionBoxes) {
      const box = document.getElementById(boxId);
      if (box.style.display === 'block') {
        activeDescription = box;
        break;
      }
    }
    if (activeDescription) {
      activeDescription.focus();
      document.execCommand('fontName', false, font);
    }
  }
}

function downloadDescription() {
  const descriptionBoxes = [
    'createCompanyDescription',
    'createIndividualDescription',
    'passCompanyDescription',
    'passIndividualDescription'
  ];
  let activeDescription = null;
  for (const boxId of descriptionBoxes) {
    const box = document.getElementById(boxId);
    if (box.style.display === 'block') {
      activeDescription = box;
      break;
    }
  }
  if (activeDescription) {
    const description = activeDescription.innerHTML;
    const blob = new Blob([description], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'description.html';
    a.click();
    URL.revokeObjectURL(url);
  } else {
    alert('No description box is currently visible to download.');
  }
}

function copyToClipboard() {
  const descriptionBoxes = [
    'createCompanyDescription',
    'createIndividualDescription',
    'passCompanyDescription',
    'passIndividualDescription'
  ];
  let activeDescription = null;
  for (const boxId of descriptionBoxes) {
    const box = document.getElementById(boxId);
    if (box.style.display === 'block') {
      activeDescription = box;
      break;
    }
  }
  if (activeDescription) {
    const description = activeDescription.innerHTML;
    navigator.clipboard.writeText(description).then(() => {
      alert('Description copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy:', err);
      alert('Failed to copy description to clipboard.');
    });
  } else {
    alert('No description box is currently visible to copy.');
  }
}

let cropper;

function openCropper(type) {
  const fileInput = type === 'passCompany' ? document.getElementById('passPosterUpload') : document.getElementById('passIndividualPosterUpload');
  const modal = document.getElementById('cropperModal');
  const image = document.getElementById('cropperImage');
  const container = document.getElementById('cropperContainer');
  const descriptionBox = type === 'passCompany' ? document.getElementById('passCompanyDescription') : document.getElementById('passIndividualDescription');

  if (fileInput.files && fileInput.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      image.src = e.target.result;
      modal.style.display = 'block';
      container.style.display = 'block';

      if (cropper) {
        cropper.destroy();
      }

      image.onload = function() {
        cropper = new Cropper(image, {
          aspectRatio: NaN,
          viewMode: 1,
          autoCropArea: 1,
          movable: true,
          rotatable: false,
          scalable: false,
          zoomable: true,
          background: false
        });
      };
    };
    reader.readAsDataURL(fileInput.files[0]);
    if (descriptionBox) descriptionBox.style.display = 'block';
  }
}

async function cropImage() {
  if (cropper) {
    const canvas = cropper.getCroppedCanvas();
    const modal = document.getElementById('cropperModal');
    const companyType = document.getElementById('passCompanyForm').style.display === 'block' ? 'passCompany' : 'passIndividual';
    const descriptionBox = companyType === 'passCompany' ? document.getElementById('passCompanyDescription') : document.getElementById('passIndividualDescription');
    const extractedTextInput = document.getElementById(`extractedText_${companyType}`);

    if (!canvas) {
      console.error('No cropped canvas available');
      return;
    }

    canvas.toBlob(async (blob) => {
      if (!blob) {
        console.error('Failed to convert canvas to blob');
        return;
      }

      const formData = new FormData();
      formData.append('image', blob, 'cropped-image.png');
      console.log('Sending image to /extract-text:', blob.size, 'bytes');

      try {
        const response = await fetch('/extract-text', {
          method: 'POST',
          body: formData
        });

        console.log('Server response status:', response.status);
        if (response.ok) {
          const result = await response.json();
          const extractedText = result.text || '';
          extractedTextInput.value = extractedText;
          console.log('Updated extractedTextInput:', extractedTextInput.value);
          if (descriptionBox && extractedText) {
            descriptionBox.innerHTML = extractedText;
          }
          console.log('Extracted text:', extractedText);
          generatePassWithAI();
        } else {
          const errorText = await response.text();
          console.error('Text extraction failed:', response.status, errorText);
          descriptionBox.innerHTML = 'Failed to extract text from image.';
        }
      } catch (error) {
        console.error('Error during fetch:', error.message);
        descriptionBox.innerHTML = `An error occurred: ${error.message}`;
      }

      modal.style.display = 'none';
      cropper.destroy();
      cropper = null;
    }, 'image/png');
  }
}

function closeCropper() {
  const modal = document.getElementById('cropperModal');
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
  modal.style.display = 'none';
}