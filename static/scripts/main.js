document.addEventListener('DOMContentLoaded', () => {
    const userDropdown = document.querySelector('.user')

    const userDropdownToggle = () => {
        const dropdown = document.querySelector('.dropdown')
        dropdown.classList.toggle('enable')
        dropdown.classList.toggle('disable')
    }

    userDropdown.addEventListener('click', userDropdownToggle)
})